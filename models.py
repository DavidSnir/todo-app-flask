class Task:
    
    id = 0
    
    def __init__(self,title:str = "untitled",is_complete: bool = False):
        Task.id += 1
        self.id: int = Task.id
        self.title: str = title
        self.is_complete: bool = is_complete
        
    def to_json(self):
        return {
            "task_id": self.id,
            "title": self.title,
            "is_complete": self.is_complete
        }