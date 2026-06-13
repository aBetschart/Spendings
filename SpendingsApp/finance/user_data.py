from dataclasses import dataclass

@dataclass(frozen=True)    
class UserData:
    id: int
    name: str

    def __eq__(self, value):
        if not isinstance(value, UserData):
            return False

        return self.id == value.id and self.name == value.name
    
    def __repr__(self):
        return f"UserData(id={self.id}, name='{self.name}')"