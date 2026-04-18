import uuid

class TaskList:
    
    @classmethod
    def from_dict(cls, list_dict: dict) -> 'TaskList':
        """Needs a dictionary contains:
        ```\n{
            \n\t"title": str,
            \n\t"_id": str(UUID)
        \n}"""
        return TaskList(
            title=list_dict["title"],
            list_id=uuid.UUID(list_dict["_id"])
        )
        
    def __init__(self, title: str = "untitled", list_id: uuid.UUID = None):
        self._id: uuid.UUID = list_id if list_id else self._generate_id()
        self.title: str = title
        
    def to_json(self):
        return {
            "_id": str(self._id),
            "title": self.title
        }
        
    def _generate_id(self) -> uuid.UUID:
        return uuid.uuid4()
    
    def edit_list(self, user_data: dict):
        """gets a dictionary of fields to update
        {
            "title": str
        } edits the list and returns self"""
        for key, value in user_data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
