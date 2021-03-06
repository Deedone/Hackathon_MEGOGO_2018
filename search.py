from tkinter import *

class MainWindow(Frame):
    counter = 0
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.button = Button(self, text="Create new window", 
                                command=self.create_window)
        self.button.pack(side="top")

    def create_window(self):
        self.counter += 1
        t = Toplevel(self)
        t.wm_title("Window #%s" % self.counter)
        l = Label(t, text="This is window #%s" % self.counter)
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

if __name__ == "__main__":
    root = Tk()
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
