import tkinter
import tkinter.messagebox
from tkinter import filedialog as fd 
import tkinter.messagebox as mb
import customtkinter as ctk
import json
import os
import subprocess
import random
from tqdm import tqdm
from googletrans import Translator
import threading

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Translete:
    """docstring for Translete"""
    def __init__(self, text):
        super(Translete, self).__init__()
        self.translator = Translator(service_urls=['translate.googleapis.com'])
        self.conf_not_take = {
            "$": "Ӂ",
            "@": "✣",
            "1": "̶1̶",
            "2": "2̶",
            "3": "3̶",
            "4": "4̶",
            "5": "5̶",
            "6": "6̶",
            "7": "7̶",
            "8": "8̶",
            "9": "9̶",
            "0": "0̶"
        }
        self.init_text(text)


    def init_text(self,text):
        for (k,v) in self.conf_not_take.items():
            text = text.replace(k,v)
        self.text = text

    def translete(self,dest='ru',src=''):
        if len(src) >= 1:
            self.text = self.translator.translate(self.text, dest=dest,src=src).text
        else:
            self.text = self.translator.translate(self.text, dest=dest).text

        for (k,v) in self.conf_not_take.items():
            self.text = self.text.replace(v,k)

        return self.text



class GenerateRuJson:
    """docstring for GenerateRuJson"""
    def __init__(self, path, end_filename='ru.json'):
        super(GenerateRuJson, self).__init__()
        self.path = path
        self.ru = {}
        self.E = end_filename
        self.read_file()


    def str_to_jsonStr(self,text):
        text = "".join(list(text)[::-1]).replace(',','',1)
        return "".join(list(text)[::-1])

    def del_comments(self,file):
        a = ''
        for line in file.readlines():
            if '//' not in line:
                a+=line

        with open('test.txt','w',encoding='utf-8-sig') as f:
            f.write(a)
        return a

    def read_file(self):
        try:
            with open(f'{self.path}','r',encoding='utf-8-sig') as self.default_file:
                self.default_fileText = self.del_comments(self.default_file)
            self.defaultJson = json.loads(self.default_fileText)
            return True
        except Exception as e:
            return False

    def file_ok(self):
        return self.read_file()
            
    def JustRead(self):
        return self.defaultJson

    def generate(self):
        for (key,value) in tqdm(self.defaultJson.items()):
            trgoogle = Translete(str(value))
            self.ru[key] = trgoogle.translete()

        with open('{}'.format(self.path.replace(self.path.split("/")[-1],self.E)),'w',encoding='utf-8-sig') as endl_file:
            json.dump(self.ru,endl_file,ensure_ascii=False,indent=4)


class MyProgressBar(ctk.CTkProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # create the text item in the internal canvas
        self._canvas.create_text(0, 0, text=self._variable.get(), fill="pink",
                                 font=('Arial', 9), anchor="c", tags="progress_text")

    # override function to move the progress text at the center of the internal canvas
    def _update_dimensions_event(self, event):
        super()._update_dimensions_event(event)
        self._canvas.coords("progress_text", event.width/2, event.height/2)

    # override function to update the progress text whenever new value is set
    def set(self, val, **kwargs):
        super().set(val, **kwargs)
        self.rnds = "CharacterDialogue.{},event-{}.13,event-20{}10.0,Lan.MarriageDialogue.{},Lce6hearts.{}1,Wizard.Spouse{}Vary38,eggesitval{},lua{}.wizard,spirit{}.wizard,Claire.Spouse{}Vary".split(',')
        self._canvas.itemconfigure("progress_text", text=str(int(val))+f' % {random.choice(self.rnds).format(random.randint(0,9999999))}')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Just member this
        self.FileName = ''
        self.languagesCodes = {
            "ru": 0,
            "en": 1,
            "de": 2,
            "zh": 3,
            "es": 4,
            "kk": 5
        }
        self.dest = "".join([str(k if v == 0 else '') for (k,v) in self.languagesCodes.items()])

        # Just member This END.


        # configure window
        self.title("PyJSON AutoTranslete")
        self.geometry(f"{1100}x{780}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Опции", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, command=self.sidebar_open_FileDialog, 
            text='Выбрать файл')
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        #self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, command=self.sidebar_open_File,     text='открыть файл')
        #self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=20)
        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Настройки темы:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Размер:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = ctk.CTkEntry(self, placeholder_text="Выберите файл")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = ctk.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),
            text="Начать", command=self.start_TransleteFile
        )
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        

        # create slider and progressbar frame
        self.slider_progressbar_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=0, column=1, padx=(50, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=12)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=12)
        

        self.progressbar_1Label = ctk.CTkLabel(self.slider_progressbar_frame, text="Опции", font=ctk.CTkFont(size=20, weight="bold"))
        self.progressbar_1Label.grid(row=0, column=0, padx=0, pady=(0, 0))

        self.progressbar_1 = MyProgressBar(self.slider_progressbar_frame,mode = 'determinate',progress_color='#fa2844',variable=ctk.IntVar(value=100))
        self.progressbar_1.grid(row=1, column=0, padx=(40, 40), pady=(40, 40), sticky="ew")
        

        # create scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="На какой переводим?")
        self.scrollable_frame.grid(row=0, column=5, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_radios = []
      
        self.radio_var = tkinter.IntVar(value=0)
        
        for (name,value) in self.languagesCodes.items():
            radio_button = ctk.CTkRadioButton(master=self.scrollable_frame, variable=self.radio_var, value=value,text=name,command=self.chooseLanguage)
            radio_button.grid(row=value, column=0, pady=10, padx=0, sticky="n")
            self.scrollable_frame_radios.append(radio_button)
        
       
        

        # set default values
       
        self.progressbar_1Label.configure(text = '')
        self.progressbar_1.set(0)
    
        
        self.appearance_mode_optionemenu.set("Dark")
        
        self.scaling_optionemenu.set("100%")
       
    def update(self,val=0.0):
        while self.iterable <= self.lenght_this:
            trgoogle = Translete(str(self.rvalue[self.iterable]))
            self.ru[self.rkeys[self.iterable]] = trgoogle.translete(dest=self.dest)
            with open('{}'.format(self.FileName.replace(self.FileName.split("/")[-1],self.endFileName)),'w',encoding='utf-8-sig') as endl_file:
                json.dump(self.ru,endl_file,ensure_ascii=False,indent=4)
            self.progressbar_1Label.configure(text = self.ru[self.rkeys[self.iterable]])
            self.progressbar_1.set((self.iterable*100)/self.lenght_this)
            self.iterable+=1
            


   

    def open_DialogInfo(self,text,title="Info"):
        mb.showinfo(title, text)

    def open_DialogWarning(self,text,title="Warning!"):
        mb.showwarning(title, text)

    def open_DialogError(self,text,title="ERROR!?"):
        mb.showerror(title, text)

    def chooseLanguage(self):
        self.dest = "".join([str(k if v == int(self.radio_var.get()) else '') for (k,v) in self.languagesCodes.items()])
        print(self.dest)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def start_TransleteFile(self):
        if self.FileName == '':
            return self.open_DialogInfo('Вы не выбрали файл для перевода.')
        if len(self.entry.get()) < 1:
            return self.open_DialogInfo('Вы не выбрали новое имя файл для записи перевода.')
        if len(self.entry.get()) >= 30:
            return self.open_DialogWarning('Слишком длинное название файла! (максимум 30 символов)')

        self.endFileName = self.entry.get()+'.json'
        self.RealyYes = GenerateRuJson(path=self.FileName,end_filename=self.endFileName).JustRead()
        self.ru = {}
        self.iterable = 0
        self.lenght_this = len(self.RealyYes.items())
        self.rkeys = [k for (k,v) in self.RealyYes.items()]
        self.rvalue = [v for (k,v) in self.RealyYes.items()]
        #self.after(100, self.update,True)
        self.thread = threading.Thread(target=self.update)
        print(threading.main_thread().name)
        print(self.thread.name)
        self.thread.start()
        self.progressbar_1.configure(variable=ctk.IntVar(value=self.lenght_this))
        #while self.iterable <= self.lenght_this:
        #    self.update()


    def checkFormat(self,FileName,need='json'):
        try:
            if (need in FileName) and os.path.exists(FileName):
                return GenerateRuJson(path=self.FileName).file_ok()
        except Exception as ERROR:
            self.open_DialogError(str(ERROR),title="Exception JSON read")
            return False

    def sidebar_open_File(self):
        if self.FileName == '':
            return self.open_DialogInfo('Вы не выбрали файл для перевода.')




    def sidebar_open_FileDialog(self):
        self.FileName = fd.askopenfilename()
        print(self.FileName)
        if self.checkFormat(self.FileName):
            self.entry.configure(state="normal")
            self.entry.configure(placeholder_text="Имя выходного файла (изначально): "+self.FileName.split('/')[-1])


if __name__ == "__main__":
    app = App()
    app.mainloop()