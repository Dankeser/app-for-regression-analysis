class PropertyMixin:
    @property
    def active_user(self):
        return self.user_instance.active_user

    @active_user.setter
    def active_user(self,value):
        self.user_instance.active_user=value