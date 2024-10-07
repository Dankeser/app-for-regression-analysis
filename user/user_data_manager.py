import json
import os
from typing import NoReturn

wd = os.getcwd()
PATH = f'{wd}/data/users.json'

class UserDataLoader:
    def __init__(self):
        self.users = self.load_user_data()
        self.active_user_index = None
        self.user_key = None

    @property
    def active_user(self):
         return self.users[self.active_user_index]

    def load_user_data(self):
        with open(PATH,'r+') as file:
            if file.read() == "":
                file.write("[]")
        with open(PATH,"r") as file:
            return json.load(file)

    def update(self,new):
        with open(PATH,'w') as file:
            json.dump(new,file)
        self.users = self.load_user_data()

    def reload(self):
        self.users = self.load_user_data()

def add_user(name: str, username: str, hashed_password: str, instance: object) -> NoReturn:

    # new_user Object
    new_user = {'name': name,
                'username': username,
                'password': hashed_password,
                'content': None
                }

    instance.users.append(new_user)
    instance.update(instance.users)
