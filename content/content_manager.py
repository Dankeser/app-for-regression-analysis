from .regression import Regression
from typing import NoReturn
from sec.encryption_module import EncryptClass

class Content(EncryptClass):
    def load_content(self):
        if self.active_user['content'] is not None:
            content = self.decrypt_function(self.active_user['content'])
            return content
        else:
            return None

    def content_name_check(self,name) -> bool:
        if self.active_user['content'] is not None:
            content = self.decrypt_function(self.active_user['content'])
            for i in content:
                if i['title'] == name:
                    return False
            return True
        else:
            return True

    def new_content(self,newcontent: object) -> NoReturn:
        if self.active_user['content'] is not None:
            content = self.decrypt_function(self.active_user['content'])
            for i in content:
                if i['title'] == newcontent['title']:
                    return
            content.append(newcontent)
            content = self.encrypt_function(content)
            self.active_user['content'] = content
            self.user_instance.update(self.user_instance.users)
        else:
            self.active_user['content'] = self.encrypt_function([newcontent])
            self.user_instance.update(self.user_instance.users)

    # buttont callback
    def see_content(self,content_name: str,x_werte: list,y_werte: list, index: int) -> NoReturn:
        try:
            getattr(self,"grafik"+str(index))

        except AttributeError:
            #GrafikFrame leeren, bevor neue Grafik gepackt wird.
            for i in self.master.rightframe.grafikframe.winfo_children():
                i.forget()
            regr = Regression(self,x=x_werte,y=y_werte,title=content_name, index=index)
            regr.zeichnen()
            return
        for i in self.master.rightframe.grafikframe.winfo_children():
            i.forget()
        getattr(self, "grafik" + str(index)).pack(side="top", expand=1)

    # delete button callback
    def delete_content(self,content_name: str) -> NoReturn:
        content = self.decrypt_function(self.active_user['content'])
        for index, i in enumerate(content):
            if i['title'] == content_name:
                content.pop(index)
                self.active_user['content'] = self.encrypt_function(content)
                self.user_instance.update(self.user_instance.users)
        self.dynamic_buttons()
