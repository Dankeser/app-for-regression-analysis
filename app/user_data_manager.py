import json
import os
wd = os.getcwd()
PATH = f'{wd[:-4]}/data/users.json'

class UserDataLoader:
    def __init__(self):
        self.users = self.load_user_data()
        self.active_user_index = None
        self.user_key = None

    @property
    def active_user(self):
         return self.users[self.active_user_index]

    def load_user_data(self):
        with open(PATH,'r') as file:
            return json.load(file)

    def update(self,new):
        with open(PATH,'w') as file:
            json.dump(new,file)
        self.users = self.load_user_data()

    def reload(self):
        with open(PATH,'r') as file:
            self.users = json.load(file)
