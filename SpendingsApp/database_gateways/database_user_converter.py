
from django.contrib.auth.models import User

from SpendingsApp.finance.user_data import UserData
from SpendingsApp.request_data_preparation.user_converter import UserConverter


class DatabaseUserConverter(UserConverter):

    def convert_to_user(self, input: any) -> UserData:
        try:
            return self._try_convert_options(input)
        except ValueError:
            message = f"Cannot convert input {input} to UserData."
            raise ValueError(message)


    def _try_convert_options(self, input: any) -> UserData:
        if isinstance(input, UserData):
            return input
        
        if isinstance(input, User):
            return self._convert_to_user_data(input)
        
        if isinstance(input, int):
            user = User.objects.get(id=int(input))
            return self._convert_to_user_data(user)
        
        if isinstance(input, str):
            user = User.objects.get(username=str(input))
            return self._convert_to_user_data(user)
        
        if isinstance(input, dict):
            if 'id' in input:
                user = User.objects.get(id=int(input['id']))
                return self._convert_to_user_data(user)
            if 'username' in input:
                user = User.objects.get(username=str(input['username']))
                return self._convert_to_user_data(user)

        raise ValueError()

    def _convert_to_user_data(self, user: User) -> UserData:
        return UserData(id=user.id, name=user.username)