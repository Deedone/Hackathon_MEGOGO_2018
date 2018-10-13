from tkinter import *
from PIL import ImageTk,Image  
from html.parser import HTMLParser
from bs4 import BeautifulSoup

import tkinter.ttk as ttk
import urllib
import math
from html_request import *
from moviepy.editor import *
from mediaplayer import Player
import vlc
import sys
import getStreamFile.getStreamFile
from segment_processor import SegmentManager

#import translator.translateSubtitles

current_page = 1
empty_string = "                                                                                         "
width=900
height=500
frame = 1

class Delegate:

    def __init__(self, func, url):
        self.func = func
        self.url = url

    def __call__(self):
        self.func(self.url)
        

class Application(Frame):
    counter = 1
    """ GUI для обработки объектов на форме """
    
    def __init__(self, master, frame):
        """ Конструктор класса Application для фрейма """
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets(frame)

    def get_letter_count(self, word):
        counter = 0
        for letter in word:
            counter = counter + 1
        return counter    
    
    def create_widgets(self, frame):
        """ Создать виджеты для фрейма """
        # Виджет поиска
        self.find = StringVar()
        self.find_entry = Entry(textvariable = self.find)
        self.find_entry.grid(row = 0, column = 1,ipadx = 40, padx = 10, pady = 10)
        # Кнопка поиска
        self.btn_find = Button(self,
                          text = "Find",
                          background="#555",     # фоновый цвет кнопки
                          foreground="#ccc",     # цвет текста
                          padx="20",             # отступ от границ до содержимого по горизонтали
                          pady="8",              # отступ от границ до содержимого по вертикали
                          font="16"              # высота шрифта
                          )
        self.btn_find.grid(row = 0, column = 0)
        
        # Сортирвока по рейтингу, популярности, недавности
        # Выбор жанра
        items = ["Популярность", "Рейтинг", "Недавности"]
        self.list = ttk.Combobox( values = items)
        self.list.grid(row = 0, column = 2)
        
       # Таблица выбора фильмов
        currentIndex = 0
        
        global current_page
        global old_text_list
        
        for r in range(1,3):
           for c in range(6):
               # Загрузка изображений
               # Изменение размера картинки на нужный
               self.img = Image.open("Program Files\\Pictures\\" + str(currentIndex) + ".jpg")
               self.img = self.img.resize((200, 300), Image.ANTIALIAS) #200, 100 Misha's params
               # Добавление в PhotoImage 
               self.photo = ImageTk.PhotoImage(self.img)
               # Загружаем фото на форму через label
               # Просто tkinter не поддерживает прямую загрузку на форму фото
               file = open("Program Files\\HtmlLink\\" + str((r-1)*6 + c) + ".htmlLink", "r")
               print()
             
               
               self.button = Button(frame,
                                    image = self.photo,
                                    background="#555",     # фоновый цвет кнопки
                                    foreground="#ccc",     # цвет текста
                                    padx="20",             # отступ от границ до содержимого по горизонтали
                                    pady="8",              # отступ от границ до содержимого по вертикали
                                    font="16",
                                    command = Delegate(self.__create_windows, file.read())
                                    )
               self.button.image = self.photo 
               self.button.grid(row = (2*r - 1), column = 1 + c, ipadx = 10, ipady = 5, padx = 10, pady = 5)
               file.close()
               # Под каждой фотографией есть 2 вещи                
               # 1. Надпись
               # 2. Рейтинг
               #открытие файла и чтение иz него
               data = self.read_file(currentIndex = currentIndex)
               print("dataCount: " + str(self.get_letter_count(data)))
               #заносим в ЛЕЙБЛ инфу про фильм
               self.create_text_under_photo(data=data, r=r, c=c)
               currentIndex = currentIndex + 1
             
        # Кнопка переключение страницu
               self.create_btn_before()
               self.create_btn_next()
    
    def read_file(self, currentIndex):
        """ Read filne that contains photos + description """
        handle = open("Program Files\\TvInfo\\" + str(currentIndex) + ".tvInfo", "r")
        data = handle.read()  #reading description
        handle.close()
        return data

    def clear_text(self):
        """ Celar space for new label(text below movie pic) """
        global empty_string
                
        for r in range(1,3):
           for c in range(6):
               self.create_text_under_photo(data = empty_string,r=r,c=c) 
        

    def create_text_under_photo(self, data, r, c):
        global frame
        self.lbl = Label(frame, text = data)
        self.lbl.grid(row = 2*r, column = 1 + c, ipadx = 2, ipady = 2, padx = 2, pady = 2)
               
    def create_btn_before(self):
        global current_page
        global frame
        
        page_before_txt = current_page - 1
        if current_page == 1:
            page_before_txt = current_page

        btn_page_before = Button(
                          text = page_before_txt,
                          background="#555",     # фоновый цвет кнопки
                          foreground="#ccc",     # цвет текста
                          padx="10",             # отступ от границ до содержимого по горизонтали
                          pady="5",              # отступ от границ до содержимого по вертикали
                          font="11",             # высота шрифта
                          command = self.priv_page
                          )
        btn_page_before.place(y = 0,x = 550)

    def create_btn_next(self):
        global current_page
        global frame
        page_next_txt = current_page + 1

        btn_page_next = Button(
                          text = page_next_txt,
                          background="#555",     # фоновый цвет кнопки
                          foreground="#ccc",     # цвет текста
                          padx="10",             # отступ от границ до содержимого по горизонтали
                          pady="5",              # отступ от границ до содержимого по вертикали
                          font="11"              # высота шрифта
                      
                          )
        
        btn_page_next.place(y = 0,x = 600)

    def next_page(self):
        global current_page
        global frame
        self.clear_text()
        current_page = current_page + 1
        htmpRequest = HTMLdata(current_page)
        self.create_widgets(frame=frame)
        
    def _quit(self):
        print("_quit: bye")
        root = Tk()
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
        os._exit(1)
    
    def __create_windows(self, url):
        """
        t = Toplevel(self)
        t.wm_title("Wiasdasdndow #%s" % self.counter)
        l = Label(t, text="This is window #%s" % self.counter)
        l.pack(side="top", fill="both", expand=True, padx=width, pady=height)
        print(vlc.__dict__)
        player = vlc.MediaPlayer("http://185.38.12.43/sec/1539468805/343534338d064aef7a0d8e8e23411662971fe1ea4222f4df/ivs/77/65/2de78733cbed/hls/tracks-4,5/index.m3u8")
        player.play()
        self.counter += 1
        
        root = Tk_get_root()
        root.protocol("WM_DELETE_WINDOW", _quit)

        player = Player(root, title="Video player(VLC)")
        # show the player window centred and run the application
        """

        #
        # 1. Load Selenium
        link_m3u8 = getStreamFile.getStreamFile.getStreamFile(url)
        print(link_m3u8)
        # 2. Get m3u8 link
        #
        SM = SegmentManager(link_m3u8)
        
        root1 = Tk()
        root1.protocol("WM_DELETE_WINDOW", self._quit)
        player = Player(root1, SM, link_m3u8, title="Video player(VLC)")
        
        
        root1.mainloop()

         
    def priv_page(self):
        global current_page
        global frame
       
        if current_page != 1:
            self.clear_text()
            current_page = current_page - 1
            htmpRequest = HTMLdata(current_page)
            self.create_widgets(frame=frame)
 

        
def myfunction(event):
    global height
    global width
    canvas.configure(scrollregion=canvas.bbox("all"),width=width-50,height=height-180)

        
             
htmpRequest = HTMLdata(1)
root = Tk()

root.configure(background='black')
myframe=Frame(root,relief=GROOVE,width=50,height=100,bd=1)
myframe.place(x=10,y=50)

canvas=Canvas(myframe)
frame=Frame(canvas)
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
myscrollbarX=Scrollbar(myframe,orient="horizontal",command=canvas.xview)
canvas.configure(yscrollcommand=myscrollbar.set)
canvas.configure(xscrollcommand=myscrollbarX.set)

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

myscrollbar.pack(side="right",fill="y")
myscrollbarX.pack(side="bottom",fill="x")
canvas.pack(side="left")
canvas.create_window((0,0),window=frame,anchor='nw')
frame.bind("<Configure>",myfunction)

root.title("Movies and TV series")
print(root.winfo_screenwidth())
print(root.winfo_screenheight())

app = Application(root, frame)

root.geometry(str(root.winfo_screenwidth()) + "x" + str(root.winfo_screenheight()))
root.mainloop()
