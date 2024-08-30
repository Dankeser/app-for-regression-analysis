import customtkinter as ctk
from typing import NoReturn

from content.mytoolbox import FrameChange, LoginCheck
from user.property_class import PropertyMixin
from content.content_manager import Content

class LoginFrame(ctk.CTkFrame, FrameChange, LoginCheck, Content, PropertyMixin):
    def __init__(self,master,user_data_instance):
        super().__init__(master,width=200,height=300)
        self.master = master
        self.user_instance = user_data_instance
        self.popup = None
        self.grid_columnconfigure(0,weight=1)

        self.wilkommen_label=ctk.CTkLabel(self,text='Welcome,\n please sign in.',width=250,text_color="gray100",font=ctk.CTkFont(size=20),padx=20,pady=20)
        self.wilkommen_label.grid(row=0,column=0,padx=10,pady=(10,0))

        self.benutzername_label=ctk.CTkLabel(self,text_color="gray100",text='Username:',anchor='w')
        self.benutzername_label.grid(row=1,column=0,padx=10,pady=(20,0))

        self.benutzername=ctk.CTkEntry(self)
        self.benutzername.grid(row=2,column=0,padx=10)

        self.benutzername_label.configure(width=self.benutzername.cget('width'))

        self.passwort_label = ctk.CTkLabel(self,text_color="gray100", text='Password:',anchor='w')
        self.passwort_label.grid(row=3, column=0, padx=10, pady=(10, 0))

        self.passwort=ctk.CTkEntry(self,show='*',)
        self.passwort.grid(row=4,column=0,padx=10)

        self.passwort_label.configure(width=self.passwort.cget('width'))

        self.login_button=ctk.CTkButton(self,text_color="gray100",text='login', command=self.login_callback)
        self.login_button.grid(row=5,column=0,padx=10,pady=(10))

        self.register_button=ctk.CTkButton(self,text_color="gray100",text='create an account',command=self.register_callback,fg_color=('gray50','gray15'),hover_color=('gray60','gray20'))
        self.register_button.grid(row=6,column=0,pady=(10,20))

    def login_callback(self) -> NoReturn:
        if self.login_check(self.benutzername,self.passwort):
            self.load_content()
            self.change_to_mainframe(self)

    def register_callback(self) -> NoReturn:
        self.change_the_frame(self,self.master.registerframe)