import customtkinter as ctk
import matplotlib
from typing import NoReturn
from customtkinter import filedialog as fd
import pandas

from .content_manager import Content
from .popup_frame import PopUpFrame
from user.property_class import PropertyMixin

matplotlib.use('TkAgg')

class GrafikFrame(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master

class RightBottomFrame(ctk.CTkFrame,Content,PropertyMixin):
    def __init__(self,master):
        super().__init__(master,corner_radius=0)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.master=master
        self.user_instance=self.master.user_instance
        self.selected=self.master.master.leftframe.selected
        self.content= self.load_content()
        self.filename = None

        self.filebutton=ctk.CTkButton(self,text='select .csv file',command=self.select_file)
        self.filebutton.grid(row=0,column=1,padx=10,pady=10)

        self.entry = ctk.CTkEntry(self,placeholder_text='give a titel')
        self.entry.grid(row=0, column=3, padx=10, pady=10)

        self.create=ctk.CTkButton(self,text='draw',command=self.create_regression)
        self.create.grid(row=0,column=4,padx=10,pady=10)

    def g(self) -> NoReturn:
        scalex = (self.popup.cget('width')/2) / self.master.winfo_width()
        scaley = (self.popup.cget('height')/2) / self.master.winfo_height()
        self.popup.place(in_=self.master.master, relx=0.5 - scalex, rely=0.5 - scaley)

    def create_regression(self):
        if self.filename is None:
            self.popup = PopUpFrame(self.master.master, 'Please select a file.')
            self.g()
            return
        if len(self.entry.get()) == 0:
            self.popup = PopUpFrame(self.master.master,'Please give a titel.')
            self.g()
            return
        if not self.content_name_check(self.entry.get()):
            self.popup = PopUpFrame(self.master.master, 'The graph is already exist.')
            self.g()
            return
        else:
            try:
                data = pandas.read_csv(self.filename)
                content_object = {
                    'title': self.entry.get(),
                    'x': list(map(float, data[data.columns[0]].tolist())),
                    'y': list(map(float, data[data.columns[1]].tolist()))
                }
            except Exception:
                self.popup = PopUpFrame(self.master.master, str(Exception))
                self.g()
                return

            self.new_content(content_object)
            self.content = self.load_content()
            self.master.master.content = self.load_content()
            self.master.master.leftframe.dynamic_buttons()

    def select_file(self):
        filetypes = [('csv files', '*.csv')]
        self.filename = fd.askopenfilename(title='open a .csv file', filetypes=filetypes,initialdir='/')
        self.label = ctk.CTkLabel(self,text=self.filename)
        self.label.grid(row=0,column=2,padx=10,pady=10)

class RightFrame(ctk.CTkFrame, PropertyMixin):
    def __init__(self,master):
        super().__init__(master)
        self.master=master
        self.user_instance = self.master.user_instance
        self.grafikframe=GrafikFrame(self)
        self.grafikframe.pack(side='top',padx=10,pady=10,expand=1,fill='both')

        self.bottomframe= RightBottomFrame(self,)
        self.bottomframe.pack(side='bottom',padx=10,pady=10,fill='x')


class LeftFrame(ctk.CTkScrollableFrame, Content, PropertyMixin):
    def __init__(self,master):
        super().__init__(master,corner_radius=0)
        self.master = master
        self.user_instance = self.master.user_instance
        self.selected=None
        self.dynamic_buttons()
        self.grid_columnconfigure((0,1,2),weight=1)

    #Create buttons in left frame that show graphs.
    def dynamic_buttons(self) -> NoReturn:
        if self.load_content() is not None:
            for i in self.winfo_children():
                i.destroy()
            content = self.load_content()
            #zu see_content() Funktion, die in button_callback() liegt, wird auch index gesendet, um jedes mal nicht wieder gleiche Grafik von neu aus zu bauen.
            for index,i in enumerate(content):
                titel=i['title']
                x_werte = i['x']
                y_werte = i['y']
                if self.selected == titel:
                    ctk.CTkButton(self, text=titel, corner_radius=0,command=lambda t=titel, x=x_werte, y=y_werte, i=index: self.button_callback(t,x,y,i), width=100).grid(row=index, column=0,padx=(10,0),pady=(10,0), sticky='ew', columnspan=2)

                    ctk.CTkButton(self,fg_color='#f12323',hover=False, text='destroy', corner_radius=0,command=lambda t=titel, i=index: self.delete_button_callback(t,i), width=20).grid(row=index,column=2,padx=(0,10),pady=(10,0), sticky='ew')
                else:
                    ctk.CTkButton(self,text=titel,corner_radius=0, command=lambda t=titel, x=x_werte, y=y_werte, i=index: self.button_callback(t,x,y,i), width=100).grid(row=index,column=0,padx=10,pady=(10,0), sticky='ew', columnspan=2)

                    ctk.CTkButton(self, fg_color='#f12323', hover=False, text='destroy',corner_radius=0,command=lambda t=titel, i=index: self.delete_button_callback(t,i), width=20).grid(row=index, column=2, padx=(0, 10),pady=(10, 0),sticky='ew')

    def button_callback(self,t,x,y,i):
        self.selected=t
        self.see_content(t, x, y,i)

    def delete_button_callback(self,t,i):
        if self.selected == t:
            getattr(self,"grafik"+str(i)).destroy()
            setattr(self,"grafik"+str(i),None)
        self.delete_content(t)
        self.dynamic_buttons()

class MainFrame(ctk.CTkFrame,Content, PropertyMixin):
    def __init__(self,master,user_data_instance: object):
        super().__init__(master)
        self.master = master
        self.master.title("Linear-Regression App")
        self.user_instance = user_data_instance

        self.leftframe = LeftFrame(self)
        self.leftframe.pack(fill='y',side='left')

        self.rightframe = RightFrame(self)
        self.rightframe.pack(fill='both',expand=1)
