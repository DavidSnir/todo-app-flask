import uuid

class Task:
            
    def __init__(self, title: str = "untitled", is_complete: bool = None,task_id: uuid.UUID = None ,parent_id: uuid.UUID = None):
        self.parent_id: uuid.UUID = parent_id
        if not task_id:
            self._id: uuid.UUID = self._generate_id()
        else:
            self._id: uuid.UUID = task_id

        self.title: str = title
        
        if not is_complete:
            self.is_complete: bool = False
        else:
            self.is_complete: bool = True
        
    def to_json(self):
        return {
            "_id": str(self._id),
            "parent_id": str(self.parent_id),
            "title": self.title,
            "is_complete": self.is_complete
        }
    def _generate_id(self) -> None:
        return uuid.uuid4()
    
    def create_sub_task(self,title:str = None,is_complete: bool = None):
        new_task = Task(title=title,is_complete=is_complete,parent_id=self._id)
        return new_task
        
    def is_sub_task_exist(self,_id: uuid.UUID) -> bool:
        pass
    
    def edit_task(self, user_data: dict):
        """gets the task and a user data in dictionary
        `{
            "title": str,
            "is_complete": bool
        }` edits the task and returns a refrence for it (task)"""
        for key, value in user_data.items():
            setattr(self,key,value)
        return self

    # def remove_task(self) -> None:
    #     """remove task if it doesnt have sub task"""
    #     # if not self._id in Task.tasks_id_by_parent_id_list:
    #     #     Task.tasks_by__id_list.pop(self._id)
    #     # else:
    #     #     raise ValueError("Task have subtasks, the remove_task_and_sub_task function is needed")
    #     pass
    
    # def remove_task_and_sub_task(self) -> None:
    #     """remove task and it's sub tasks recursivly"""
    #     sub_tasks_id = Task.tasks_id_by_parent_id_list[self._id]
    #     if sub_tasks_id:
    #         for _id in sub_tasks_id:
    #             task: Task = Task.get_task_by_id(_id)
    #             task.remove_task_and_sub_task()
    #     else:
    #         self.remove_task()
        
    
# class Task_List:
    
#     task_lists: dict[str, Task_List] = {}
    
#     def __init__(self, name):
#         if self.is_e(name):
#             self.name: str = name
#             self.id: uuid = self._generate_id()
#             self.tasks: list[Task] = []
#             self._add_list(self)
#         else:
#             raise ValueError("list name already exists")
            
#     def is_exist(name: str):
#         return name.lower() in Task_List.task_lists
    
#     def _generate_id(self) -> uuid:
#         return uuid.uuid4()
    
