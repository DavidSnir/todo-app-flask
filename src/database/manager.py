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
    
    def get_task_by_id(self, task_id: str)->Task:
        task_dict = self.collection.find_one(filter={"_id":task_id})
        return Task.from_dict(task_dict)

    def get_sub_tasks(self, parent_task: Task)->list[Task]:
        sub_tasks_json = self.collection.find({"parent_id":str(parent_task._id)})
        sub_task_list: list[Task] = []
        
        for task_dict in sub_tasks_json:
            sub_task_list.append(Task.from_dict(task_dict))
            
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
