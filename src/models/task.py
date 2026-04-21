import uuid

class Task:
    
    @classmethod
    def from_dict(cls,task_dict: dict) -> "Task":
        """Needs a dictionary contains:
        ```\n{
            \n\t"title": str,
            \n\t"is_complete": bool,
            \n\t"_id": str(UUID),
            \n\t"parent_id": str(UUID) | None
        \n}"""
        try:
            parent_id = uuid.UUID(task_dict["parent_id"])
        except:
            parent_id = None
        return cls(
            title=task_dict["title"],
            is_complete=task_dict["is_complete"],
            task_id=uuid.UUID(task_dict["_id"]),
            parent_id=parent_id
        )
        
    def __init__(self, title: str = "untitled", is_complete: bool = False, task_id: uuid.UUID = None, parent_id: uuid.UUID = None):
        self.parent_id: uuid.UUID | None = parent_id
        self._id: uuid.UUID = task_id if task_id else self._generate_id()
        self.title: str = title
        self.is_complete: bool = is_complete
        
    def to_json(self):
        return {
            "_id": str(self._id),
            "parent_id": str(self.parent_id),
            "title": self.title,
            "is_complete": self.is_complete
        }
        
    def _generate_id(self) -> uuid.UUID:
        return uuid.uuid4()
    
    def create_sub_task(self, title: str = None, is_complete: bool = False):
        new_task = Task(title=title, is_complete=is_complete, parent_id=self._id)
        return new_task
        
    def edit_task(self, user_data: dict):
        """gets a dictionary of fields to update
        {
            "title": str,
            "is_complete": bool
        } edits the task and returns self"""
        for key, value in user_data.items():
            if hasattr(self, key):
                setattr(self, key, value)
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
    
