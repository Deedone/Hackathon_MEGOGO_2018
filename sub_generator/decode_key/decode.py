

import tkinter as tk
from PIL import Image, ImageTk

def callback(e):
    img2 = ImageTk.PhotoImage(Image.open("test.jpg"))
    panel.configure(image=img2)
    panel.image = img2

def run():
    print('work')
root = tk.Tk()

img = ImageTk.PhotoImage(Image.open("test.jpg"))
panel = tk.Label(root, image=img, command = run)
panel.pack(side="bottom", fill="both", expand="yes")



root.bind("<Return>", callback)
root.mainloop()
