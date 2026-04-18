from src.models.task import Task
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
            
            

