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
        tasks_obj: list[Task] = []
        for task_json in tasks_json:
            try:
                parent_id = UUID(task_json["id"])
            except:
                parent_id = None
            finally: 
                tasks_obj.append(Task(
                    title=task_json["title"],
                    is_complete=task_json["is_complete"],
                    task_id=UUID(task_json["_id"]),
                    parent_id=parent_id
                ))
        return tasks_obj
    
    def get_task_by_id(self, task_id: str)->Task:
        task_json = self.collection.find_one(filter={"_id":task_id})
        try:
            parent_id = UUID(task_json["id"])
        except:
            parent_id = None
        finally: 
            return Task(
                title=task_json["title"],
                is_complete=task_json["is_complete"],
                task_id=UUID(task_json["_id"]),
                parent_id=parent_id
            )

    def get_sub_tasks(self, parent_task: Task)->list[Task]:
        sub_tasks_json = self.collection.find({"parent_id":str(parent_task._id)})
        sub_task_list: list[Task] = []
        for task_json in sub_tasks_json:
            try:
                parent_id = UUID(task_json["id"])
            except:
                parent_id = None
            finally: 
                sub_task_list.append(Task(
                    title=task_json["title"],
                    is_complete=task_json["is_complete"],
                    task_id=UUID(task_json["_id"]),
                    parent_id=parent_id
                ))
        return sub_task_list

    def add_task(self, task: Task)->bool:
        result = self.collection.insert_one(task.to_json())
        return result.acknowledged
        

    def edit_task(self, task: Task)->bool:
        result = self.collection.find_one_and_replace(
            {"_id":str(task._id)},
            task.to_json()
        )
        return result

    def remove_task(tas: Task):
        # TODO: update the tasks index of parents
        pass
