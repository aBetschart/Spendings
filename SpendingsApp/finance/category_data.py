from dataclasses import dataclass

@dataclass
class CategoryData:
    id: int
    name: str

    def __eq__(self, value):
        if not isinstance(value, CategoryData):
            return False

        return self.id == value.id and self.name == value.name
    
    def __repr__(self):
        return f"CategoryData(id={self.id}, name='{self.name}')"