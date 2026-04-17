from models.task import Task

class TaskManager:
    def __init__(self, db_collection):
        self.collection = db_collection