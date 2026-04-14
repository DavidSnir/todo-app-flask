import uuid
class Task:
        
    def __init__(self,title:str = "untitled",is_complete: bool = False):
        self.id: str = self._generate_id()
        self.title: str = title
        self.is_complete: bool = is_complete
        
    def to_json(self):
        return {
            "task_id": self.id,
            "title": self.title,
            "is_complete": self.is_complete
        }
    def _generate_id(self):
        return str(uuid.uuid4())