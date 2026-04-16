import uuid
class Task:
        
    def __init__(self,title:str = "untitled",is_complete: bool = False):
        self.id: str = self._generate_id()
        self.title: str = title
        self.is_complete: bool = is_complete
        
    def to_json(self):
        return {
            "task_id": str(self.id),
            "title": self.title,
            "is_complete": self.is_complete
        }
    def _generate_id(self):
        return uuid.uuid4()
    
    
class Task_List:
    
    task_lists: dict[str, Task_List] = {
        
    }
    
    def __init__(self, name):
        self.name = name
        self.id = self._generate_id()
        self.tasks: list[Task] = []
    
    def _generate_id(self) -> uuid:
        return uuid.uuid4()
    
tasks_list: list[Task] =[
    Task("Learn Flask"),
    Task("Build App"),
    Task("Test With Postman",is_complete=True)
]

def get_all_tasks() -> list[Task]:
    """returns a list of the tasks list"""
    global tasks_list
    result: list = []
    for task in tasks_list:
        result.append(task.to_json())
    return result

def get_task_by_id(task_id: str) -> Task:
    """return the task with same id as inputed if exists, if not return `None`"""
    result_task: Task = None
    
    # searches fot the right task
    # TODO: change tasks_list var to dict for faster searching
    for task in tasks_list:
        if task_id == task.id:
            result_task = task
    return result_task

def create_task(task_name: str= None, is_complete: bool= None) -> Task:
    """get string name and status (optional) and adds the task to the task list. Returns the new_task cobject created"""
    if not(task_name or is_complete):
        new_task = Task()
    elif not task_name:
        new_task = Task(is_complete=is_complete)
    elif not is_complete:
        new_task = Task(task_name)
        
    tasks_list.append(new_task)
    return new_task

def edit_task(task: Task, user_data: dict) -> None:
    """gets the task and a user data in dictionary
    `{
        "title": str,
        "is_complete": bool
    }` edits the task and returns a refrence for it (task)"""
    for key, value in user_data.items():
        setattr(task,key,value)
    return task

def remove_task(task: Task) -> None:
    tasks_list.remove(task)