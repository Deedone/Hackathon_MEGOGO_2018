from PIL import ImageTk,Image 
from tkinter import *

class Loop:

    def __init__(self):
        i  = 0
        while i < 255:
            i +=1
            if i >= 255:
                i = 0
        


root = Tk()
i = 0
for i in range(255):
    mycolor = '#%02x%02x%02x' % ((64+i)%255, (204+i)%255, (208+i)%255)
    root.configure(background=mycolor)
root.mainloop()
