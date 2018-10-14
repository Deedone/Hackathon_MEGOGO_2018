from tkinter import *
import os
from PIL import ImageTk,Image  
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from urllib.request import *

import tkinter.ttk as ttk
import urllib.request
import urllib


class HTMLdata():
    
    def __init__(self, page_count):
        self.create_folders()
        self.get_img_tags('http://baskino.me/', page_count)
        #self.__start_working('http://gidonline.in/')

    def create_folders(self):
        if not os.path.exists("Program Files"):
            os.makedirs("Program Files")
        if not os.path.exists("Program Files\\Pictures"):
            os.makedirs("Program Files\\Pictures")
        if not os.path.exists("Program Files\\TvInfo"):
            os.makedirs("Program Files\\TvInfo")
        if not os.path.exists("Program Files\\HtmlLink"):
            os.makedirs("Program Files\\HtmlLink")
 

    def get_img_tags(self, url, page_number):
        movie_desc = ' '
        response =  urllib.request.urlopen(url + '/page/'+str(page_number)+'/')
        html = response.read()
        soup = BeautifulSoup(html, "html.parser" )
        film_posts = soup.find('div', {'id': 'dle-content'})
        film_lists = film_posts.find_all('div', {'class': 'shortpost'})
        i = 0
        for item in film_lists:
            movie_link = item.find('img').get('src')                        #link to images
            movie_desc = item.find('img').get('alt')                        #link to description(text)
            movie_link_html = item.find('a').get('href')
            print(movie_link + " \n "+ movie_desc + '\n' + movie_link_html)
            
            picture_full_url = str(movie_link)
            destination = 'Program Files\\Pictures\\' + str(i) + '.jpg'
            urllib.request.urlretrieve(picture_full_url, destination)      #downloading images into project folder(saving as 0-11 .jpg)
            
            handle = open('Program Files\\TvInfo\\' + str(i)+ ".tvInfo", "w")      #creating/opening file 0-11 and writing description in it
            handle.write(movie_desc)
            handle.close()
            
            handle_for_html = open('Program Files\\HtmlLink\\' + str(i)+ ".htmlLink", "w")      #creating/opening file 0-11 and writing description in it
            handle_for_html.write(movie_link_html)
            handle_for_html.close()
            
            print(str(i) + ' downloaded\n')
            i = i + 1

    def get_img_tags_new(url):
        movie_desc = ' '
    
        html = url.text
        soup = BeautifulSoup(html, "html.parser" )
        film_posts = soup.find('div', {'id': 'dle-content'})
        film_lists = film_posts.find_all('div', {'class': 'shortpost'})
        i = 0
        for item in film_lists:
            movie_link = item.find('img').get('src')                        #link to images
            movie_desc = item.find('img').get('alt')                        #link to description(text)
            movie_link_html = item.find('a').get('href')
            print(movie_link + " \n "+ movie_desc + '\n' + movie_link_html)
            
            picture_full_url = str(movie_link)
            destination = 'Program Files\\Pictures\\' + str(i) + '.jpg'
            urllib.request.urlretrieve(picture_full_url, destination)      #downloading images into project folder(saving as 0-11 .jpg)
            
            handle = open('Program Files\\TvInfo\\' + str(i)+ ".tvInfo", "w")      #creating/opening file 0-11 and writing description in it
            handle.write(movie_desc)
            handle.close()
            
            handle_for_html = open('Program Files\\HtmlLink\\' + str(i)+ ".htmlLink", "w")      #creating/opening file 0-11 and writing description in it
            handle_for_html.write(movie_link_html)
            handle_for_html.close()
            
            print(str(i) + ' downloaded\n')
            i = i + 1

    def __start_working(self, base_url):
        if base_url != None:
            response =  urllib.request.urlopen(base_url)
            html = response.read()
            soup = BeautifulSoup(html, "html.parser" )
            pages_div = soup.find('div', {'class': 'wp-pagenavi'})
            
            next_page = pages_div.find('a', {'class': 'nextpostslink'})
            next_url = next_page.get('href')
            # if(url != None){...}
            
            print(next_page)
            print(next_url)
            
            #self.get_img_tags(base_url)
            #self.start_working(next_url)
        else:
            return
    
