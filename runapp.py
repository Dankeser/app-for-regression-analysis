import customtkinter as ctk
import tkinter as tk
from sec.login_frame import LoginFrame
from sec.register_frame import RegisterFrame
from content.main_frame import MainFrame
from user.user_data_manager import UserDataLoader
from content.mytoolbox import SwitchMode
from user.property_class import PropertyMixin
from PIL import Image
import os

wd = os.getcwd()
PATH = f'{wd}/'

class MainKlasse(ctk.CTk, SwitchMode, PropertyMixin):
    def __init__(self,user_data_instance):
        super().__init__(fg_color=None)
        self.users_instance = user_data_instance
        self.title('Login Screen')
        self.minsize(width=700,height=600)
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure((0),weight=1)
        self.myimage = ctk.CTkImage(Image.open(PATH+"bg.jpg"),size=(1024,768))
        self.bg_image = ctk.CTkLabel(self,text="",image=self.myimage)
        self.bg_image.place(anchor="center",relx=0.5,rely=0.5)
        
        self.loginframe = LoginFrame(self,self.users_instance)
        self.loginframe.place(anchor="center",relx=0.5,rely=0.5)
      
        self.registerframe = RegisterFrame(self,self.users_instance)

#my additionaly settings:
ctk.set_widget_scaling(1.5)
ctk.set_window_scaling(1.5)
#ctk.DrawEngine.preferred_drawing_method='polygon_shapes'

#This is transmitted in each object
myinstance=UserDataLoader()
myapp=MainKlasse(user_data_instance=myinstance)
myapp.protocol("WM_DELETE_WINDOW", lambda: myapp.quit())
myapp.mainloop()
