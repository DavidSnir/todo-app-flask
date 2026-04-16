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
            "task_id": str(self.task_id),
            "parent_id": str(self.parent_id),
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
    
    def edit_task(self, user_data: dict) -> Task:
        """gets the task and a user data in dictionary
        `{
            "title": str,
            "is_complete": bool
        }` edits the task and returns a refrence for it (task)"""
        for key, value in user_data.items():
            setattr(self,key,value)
        return self

    def remove_task(self) -> None:
        """remove task if it doesnt have sub task"""
        if not self.task_id in Task.tasks_id_by_parent_id_list:
            Task.tasks_by_task_id_list.pop(self.task_id)
        else:
            raise ValueError("Task have subtasks, the remove_task_and_sub_task function is needed")

    def remove_task_and_sub_task(self) -> None:
        """remove task and it's sub tasks recursivly"""
        sub_tasks_id = Task.tasks_id_by_parent_id_list[self.task_id]
        if sub_tasks_id:
            for task_id in sub_tasks_id:
                task: Task = Task.get_task_by_id(task_id)
                task.remove_task_and_sub_task()
        else:
            self.remove_task()
    
    @classmethod
    def is_task_exist(task_id: uuid.UUID) -> bool:
        return task_id in Task.tasks_by_task_id_list
    
    @classmethod
    def get_task_by_id(task_id: uuid.UUID) -> Task:
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
    
    
class Task_List:
    
    task_lists: dict[str, Task_List] = {}
    
    def __init__(self, name):
        if self.is_e(name):
            self.name: str = name
            self.id: uuid = self._generate_id()
            self.tasks: list[Task] = []
            self._add_list(self)
        else:
            raise ValueError("list name already exists")
            
    def is_exist(name: str):
        return name.lower() in Task_List.task_lists
    
    def _generate_id(self) -> uuid:
        return uuid.uuid4()
    
