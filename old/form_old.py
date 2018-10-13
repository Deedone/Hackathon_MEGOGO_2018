from tkinter import *
from PIL import ImageTk,Image  
from html.parser import HTMLParser
from bs4 import BeautifulSoup

import tkinter.ttk as ttk
import urllib



class Application(Frame):
    """ GUI для обработки объектов на форме """

    def __init__(self, master):
        """ Конструктор класса Application для фрейма """
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
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
            
        for r in range(1,4):
           for c in range(3):
               # Загрузка изображений
               # Изменение размера картинки на нужный
               self.img = Image.open("test.jpg")
               self.img = self.img.resize((200, 100), Image.ANTIALIAS)
               # Добавление в PhotoImage 
               self.photo = ImageTk.PhotoImage(self.img)
               # Загружаем фото на форму через label
               # Просто tkinter не поддерживает прямую загрузку на форму фото
               self.label = Label(image = self.photo)
               self.label.image = self.photo 
               self.label.grid(row = 4 + r, column = 1 + c, ipadx = 10, ipady = 10, padx = 10, pady = 10)
               # Под каждой фотографией есть 2 вещи                
               # 1. Надпись
               # 2. Рейтинг
    
                   
               self.lbl = Label(text = "Some text")
               #self.lbl.grid(row = 4 + r, column = 1 + c)
               self.lbl.place(x = 175*r + r*70 - 70, y = (1+c)*155 + 15)

             
                
                
             
   
root = Tk()
root.title("Movies and TV series")
root.geometry("1000x550")
 
app = Application(root)
 
root.mainloop()
