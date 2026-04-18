from src.models.task import Task
from src.models.task_list import TaskList
from pymongo.collection import Collection
from pymongo import HASHED
from uuid import UUID


class TaskManager:
    def __init__(self, db_collection: Collection):
        """needs a database collection to work with"""
        self.collection = db_collection

        # create a tasks.index of parents
        self.collection.create_index(["parent_id", HASHED])

    def get_all_tasks(self) -> list[Task]:
        tasks_json = list(self.collection.find())
        tasks_list: list[Task] = []
        
        for task_dict in tasks_json:
            tasks_list.append(Task.from_dict(task_dict))

        return tasks_list
    
    def get_task_by_id(self, task_id: str) -> Task | None:
        task_dict = self.collection.find_one(filter={"_id": task_id})
        if task_dict:
            return Task.from_dict(task_dict)
        return None

    def get_sub_tasks(self, parent_task: Task) -> list[Task]:
        sub_tasks_json = self.collection.find({"parent_id": str(parent_task._id)})
        sub_task_list: list[Task] = []
        
        for task_dict in sub_tasks_json:
            sub_task_list.append(Task.from_dict(task_dict))
            
        return sub_task_list

    def add_task(self, task: Task) -> bool:
        """needs a task obj, return true if tasks was added, false if it didnt"""
        result = self.collection.insert_one(task.to_json())
        return result.acknowledged
        

    def edit_task(self, task: Task) -> bool:
        result = self.collection.find_one_and_replace(
            {"_id": str(task._id)},
            task.to_json()
        )
        return result is not None

    def remove_task(self, task: Task) -> tuple[bool, str]:
        """if task does not exists returns true, if tasks have sub task use the remove_task_and_sub_tasks"""
        if self.get_sub_tasks(task) == []:
           result = self.collection.delete_one({"_id": str(task._id)})
           return result.deleted_count > 0, str(result.raw_result)
        else:
            return False, "Task have sub tasks"
        # TODO: update the tasks index of parents
        
    def remove_task_and_sub_tasks(self, task: Task) -> tuple[bool, int]:
        """returns true and the number of removed tasks"""
        sub_tasks = self.get_sub_tasks(task)
        count = 0
        if not sub_tasks == []:
            for sub_task in sub_tasks:
                result = self.remove_task_and_sub_tasks(sub_task)
                count += result[1]
            self.remove_task(task)
            return True, count+len(sub_tasks)
        else:
            result = self.remove_task(task)
            return result[0],0

class TaskListManager:
    def __init__(self, db_collection: Collection, task_manager: TaskManager = None):
        self.collection = db_collection
        self.task_manager = task_manager

    def get_all_lists(self) -> list[TaskList]:
        lists_json = list(self.collection.find())
        lists: list[TaskList] = []
        for list_dict in lists_json:
            lists.append(TaskList.from_dict(list_dict))
        return lists

    def get_list_by_id(self, list_id: str) -> TaskList | None:
        list_dict = self.collection.find_one(filter={"_id": list_id})
        if list_dict:
            return TaskList.from_dict(list_dict)
        return None

    def add_list(self, task_list: TaskList) -> bool:
        result = self.collection.insert_one(task_list.to_json())
        return result.acknowledged

    def edit_list(self, task_list: TaskList) -> bool:
        result = self.collection.find_one_and_replace(
            {"_id": str(task_list._id)},
            task_list.to_json()
        )
        return result is not None

    def remove_list(self, task_list: TaskList) -> bool:
        if self.task_manager:
            # Set all direct tasks of this list to have no parent list
            self.task_manager.collection.update_many(
                {"parent_id": str(task_list._id)},
                {"$set": {"parent_id": "None"}}
            )
        result = self.collection.delete_one({"_id": str(task_list._id)})
        return result.deleted_count > 0

    def delete_list_and_sub_task(self, task_list: TaskList) -> tuple[bool, int]:
        """Removes the list and all tasks that have this list's ID as their parent_id, recursively."""
        if not self.task_manager:
            return False, 0
        
    
        dummy_task = Task(task_id=task_list._id)
        tasks_in_list = self.task_manager.get_sub_tasks(dummy_task)
        
        total_removed = 0
        for task in tasks_in_list:
            success, removed_count = self.task_manager.remove_task_and_sub_tasks(task)
            if success:
                total_removed += removed_count
        
        list_removed = self.remove_list(task_list)
        return list_removed, total_removed
            
            

