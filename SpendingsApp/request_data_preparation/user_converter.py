
from abc import ABC, abstractmethod

from SpendingsApp.finance.user_data import UserData


class UserConverter(ABC):
    
    @abstractmethod
    def convert_to_user(self, input: any) -> UserData:
        pass