from tkinter import *
from PIL import ImageTk,Image  
from html.parser import HTMLParser
from bs4 import BeautifulSoup


import tkinter.ttk as ttk
import urllib.request


class HTMLdata():
    
    def __init__(self):
        self.get_img_tags()

    def get_img_tags(self):
        movie_desc = ' '
        response =  urllib.request.urlopen('http://gidonline.in/')
        html = response.read()
        soup = BeautifulSoup(html, "html.parser" )
        tags = soup.findAll('img')
        movie_link = soup.find('a', {'class': 'mainlink'}).find('img').get('src')
        movie_desc = soup.find('a', {'class': 'mainlink'}).find('img').get('alt')

        print('http://gidonline.in' + movie_link + " \n "+ movie_desc)



        
app = HTMLdata()
