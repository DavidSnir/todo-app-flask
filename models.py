import uuid
class Task:
    
    tasks_by_task_id_list: dict[uuid.UUID,list[Task]] = {}
    tasks_id_by_parent_id_list:dict[uuid.UUID,list[uuid.UUID]] = {}
        
    def __init__(self, title: str = "untitled", is_complete: bool = False, parent_id: uuid.UUID = None):
        self.parent_id: uuid.UUID = parent_id
        self.task_id: uuid.UUID = self._generate_id()
        self.title: str = title
        self.is_complete: bool = is_complete
        self._add_to_tasks_by_tasks_list()
        if parent_id:
            self._add_to_tasks_by_parent_list()
        
    def to_json(self):
        return {
            "task_id": str(self.id),
            "title": self.title,
            "is_complete": self.is_complete
        }
    def _generate_id(self) -> None:
        return uuid.uuid4()
    
    def _add_to_tasks_by_tasks_list(self) -> None:
        Task.tasks_by_task_id_list[self.task_id]
    
    def _add_to_tasks_by_parent_list(self)-> None:
        Task.tasks_id_by_parent_id_list[self.parent_id].append(self.task_id)
    
    def create_sub_task(self,title:str = None,is_complete: bool = None) -> Task:
        new_task = Task(title=title,is_complete=is_complete,parent_id=self.task_id)
        return new_task
        
    def is_sub_task_exist(self,task_id: uuid.UUID) -> bool:
        sub_tasks_id_list: list[uuid.UUID] = self.tasks_id_by_parent_id_list[self.task_id]
        for sub_task_id in sub_tasks_id_list:
            if sub_task_id == task_id:
                return True
        return False
    
    @classmethod
    def is_task_exist(task_id: uuid.UUID) -> bool:
        return task_id in Task.tasks_by_task_id_list
    
    @classmethod
    def get_class_by_id(task_id: uuid.UUID) -> Task:
        if Task.is_task_exist(task_id):
            return Task.tasks_by_task_id_list[task_id]
        raise ValueError("Task does not exists")
    
    @classmethod
    def get_all_tasks() -> list[Task]:
        return list(Task.tasks_by_task_id_list.values())
    
    @classmethod
    def create_task(task_name: str = None, is_complete: bool = None) -> Task:
        new_task =Task(title=task_name,is_complete=is_complete)
        return new_task
    
    @classmethod
    def edit_task(task: Task, user_data: dict) -> Task:
        """gets the task and a user data in dictionary
        `{
            "title": str,
            "is_complete": bool
        }` edits the task and returns a refrence for it (task)"""
        for key, value in user_data.items():
            setattr(task,key,value)
        return task
    
    @classmethod
    def remove_task(task: Task) -> None:
        """remove task if it doesnt have sub task"""
        if not task.task_id in Task.tasks_id_by_parent_id_list:
            Task.tasks_by_task_id_list.pop(task.task_id)
        else:
            pass


    
class Task_List:
    
    task_lists: dict[str, Task_List] = {}
    
    def __init__(self, name):
        if self.is_e(name):
            self.name: str = name
            self.id: uuid = self._generate_id()
            self.tasks: list[Task] = []
            self._add_list(self)
        else:
            raise ValueError("user name already exists")
            
    def is_exist(name: str):
        return name.lower() in Task_List.task_lists
    
    def _generate_id(self) -> uuid:
        return uuid.uuid4()
    
    
    
    
tasks_list: list[Task] =[
    Task("Learn Flask"),
    Task("Build App"),
    Task("Test With Postman",is_complete=True)
]

# def get_all_tasks() -> list[Task]:
#     """returns a list of the tasks list"""
#     global tasks_list
#     result: list = []
#     for task in tasks_list:
#         result.append(task.to_json())
#     return result

# def get_task_by_id(task_id: str) -> Task:
#     """return the task with same id as inputed if exists, if not return `None`"""
#     result_task: Task = None
    
#     # searches fot the right task
#     # TODO: change tasks_list var to dict for faster searching
#     for task in tasks_list:
#         if task_id == task.id:
#             result_task = task
#     return result_task

# def create_task(task_name: str= None, is_complete: bool= None) -> Task:
#     """get string name and status (optional) and adds the task to the task list. Returns the new_task cobject created"""
#     if not(task_name or is_complete):
#         new_task = Task()
#     elif not task_name:
#         new_task = Task(is_complete=is_complete)
#     elif not is_complete:
#         new_task = Task(task_name)
        
#     tasks_list.append(new_task)
#     return new_task

# def edit_task(task: Task, user_data: dict) -> None:
#     """gets the task and a user data in dictionary
#     `{
#         "title": str,
#         "is_complete": bool
#     }` edits the task and returns a refrence for it (task)"""
#     for key, value in user_data.items():
#         setattr(task,key,value)
#     return task

def remove_task(task: Task) -> None:
    tasks_list.remove(task)