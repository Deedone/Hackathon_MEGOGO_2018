   1 #! /usr/bin/python
   2 # -*- coding: utf-8 -*-
   3 
   4 #
   5 # tkinter example for VLC Python bindings
   6 # Copyright (C) 2015 the VideoLAN team
   7 #
   8 # This program is free software; you can redistribute it and/or modify
   9 # it under the terms of the GNU General Public License as published by
  10 # the Free Software Foundation; either version 2 of the License, or
  11 # (at your option) any later version.
  12 #
  13 # This program is distributed in the hope that it will be useful,
  14 # but WITHOUT ANY WARRANTY; without even the implied warranty of
  15 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  16 # GNU General Public License for more details.
  17 #
  18 # You should have received a copy of the GNU General Public License
  19 # along with this program; if not, write to the Free Software
  20 # Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
  21 #
  22 """A simple example for VLC python bindings using tkinter. Uses python 3.4
  23 
  24 Author: Patrick Fay
  25 Date: 23-09-2015
  26 """
  27 
  28 # import external libraries
  29 import vlc
  30 import sys
  31 
  32 if sys.version_info[0] < 3:
  33     import Tkinter as Tk
  34     from Tkinter import ttk
  35     from Tkinter.filedialog import askopenfilename
  36 else:
  37     import tkinter as Tk
  38     from tkinter import ttk
  39     from tkinter.filedialog import askopenfilename
  40 
  41 # import standard libraries
  42 import os
  43 import pathlib
  44 from threading import Thread, Event
  45 import time
  46 import platform
  47 
  48 class ttkTimer(Thread):
  49     """a class serving same function as wxTimer... but there may be better ways to do this
  50     """
  51     def __init__(self, callback, tick):
  52         Thread.__init__(self)
  53         self.callback = callback
  54         self.stopFlag = Event()
  55         self.tick = tick
  56         self.iters = 0
  57 
  58     def run(self):
  59         while not self.stopFlag.wait(self.tick):
  60             self.iters += 1
  61             self.callback()
  62 
  63     def stop(self):
  64         self.stopFlag.set()
  65 
  66     def get(self):
  67         return self.iters
  68 
  69 class Player(Tk.Frame):
  70     """The main window has to deal with events.
  71     """
  72     def __init__(self, parent, title=None):
  73         Tk.Frame.__init__(self, parent)
  74 
  75         self.parent = parent
  76 
  77         if title == None:
  78             title = "tk_vlc"
  79         self.parent.title(title)
  80 
  81         # Menu Bar
  82         #   File Menu
  83         menubar = Tk.Menu(self.parent)
  84         self.parent.config(menu=menubar)
  85 
  86         fileMenu = Tk.Menu(menubar)
  87         fileMenu.add_command(label="Open", underline=0, command=self.OnOpen)
  88         fileMenu.add_command(label="Exit", underline=1, command=_quit)
  89         menubar.add_cascade(label="File", menu=fileMenu)
  90 
  91         # The second panel holds controls
  92         self.player = None
  93         self.videopanel = ttk.Frame(self.parent)
  94         self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH,expand=1)
  95         self.videopanel.pack(fill=Tk.BOTH,expand=1)
  96 
  97         ctrlpanel = ttk.Frame(self.parent)
  98         pause  = ttk.Button(ctrlpanel, text="Pause", command=self.OnPause)
  99         play   = ttk.Button(ctrlpanel, text="Play", command=self.OnPlay)
 100         stop   = ttk.Button(ctrlpanel, text="Stop", command=self.OnStop)
 101         volume = ttk.Button(ctrlpanel, text="Volume", command=self.OnSetVolume)
 102         pause.pack(side=Tk.LEFT)
 103         play.pack(side=Tk.LEFT)
 104         stop.pack(side=Tk.LEFT)
 105         volume.pack(side=Tk.LEFT)
 106         self.volume_var = Tk.IntVar()
 107         self.volslider = Tk.Scale(ctrlpanel, variable=self.volume_var, command=self.volume_sel,
 108                 from_=0, to=100, orient=Tk.HORIZONTAL, length=100)
 109         self.volslider.pack(side=Tk.LEFT)
 110         ctrlpanel.pack(side=Tk.BOTTOM)
 111 
 112         ctrlpanel2 = ttk.Frame(self.parent)
 113         self.scale_var = Tk.DoubleVar()
 114         self.timeslider_last_val = ""
 115         self.timeslider = Tk.Scale(ctrlpanel2, variable=self.scale_var, command=self.scale_sel,
 116                 from_=0, to=1000, orient=Tk.HORIZONTAL, length=500)
 117         self.timeslider.pack(side=Tk.BOTTOM, fill=Tk.X,expand=1)
 118         self.timeslider_last_update = time.time()
 119         ctrlpanel2.pack(side=Tk.BOTTOM,fill=Tk.X)
 120 
 121 
 122         # VLC player controls
 123         self.Instance = vlc.Instance()
 124         self.player = self.Instance.media_player_new()
 125 
 126         # below is a test, now use the File->Open file menu
 127         #media = self.Instance.media_new('output.mp4')
 128         #self.player.set_media(media)
 129         #self.player.play() # hit the player button
 130         #self.player.video_set_deinterlace(str_to_bytes('yadif'))
 131 
 132         self.timer = ttkTimer(self.OnTimer, 1.0)
 133         self.timer.start()
 134         self.parent.update()
 135 
 136         #self.player.set_hwnd(self.GetHandle()) # for windows, OnOpen does does this
 137 
 138 
 139     def OnExit(self, evt):
 140         """Closes the window.
 141         """
 142         self.Close()
 143 
 144     def OnOpen(self):
 145         """Pop up a new dialow window to choose a file, then play the selected file.
 146         """
 147         # if a file is already running, then stop it.
 148         self.OnStop()
 149 
 150         # Create a file dialog opened in the current home directory, where
 151         # you can display all kind of files, having as title "Choose a file".
 152         p = pathlib.Path(os.path.expanduser("~"))
 153         fullname =  askopenfilename(initialdir = p, title = "choose your file",filetypes = (("all files","*.*"),("mp4 files","*.mp4")))
 154         if os.path.isfile(fullname):
 155             dirname  = os.path.dirname(fullname)
 156             filename = os.path.basename(fullname)
 157             # Creation
 158             self.Media = self.Instance.media_new(str(os.path.join(dirname, filename)))
 159             self.player.set_media(self.Media)
 160             # Report the title of the file chosen
 161             #title = self.player.get_title()
 162             #  if an error was encountred while retriving the title, then use
 163             #  filename
 164             #if title == -1:
 165             #    title = filename
 166             #self.SetTitle("%s - tkVLCplayer" % title)
 167 
 168             # set the window id where to render VLC's video output
 169             if platform.system() == 'Windows':
 170                 self.player.set_hwnd(self.GetHandle())
 171             else:
 172                 self.player.set_xwindow(self.GetHandle()) # this line messes up windows
 173             # FIXME: this should be made cross-platform
 174             self.OnPlay()
 175 
 176             # set the volume slider to the current volume
 177             #self.volslider.SetValue(self.player.audio_get_volume() / 2)
 178             self.volslider.set(self.player.audio_get_volume())
 179 
 180     def OnPlay(self):
 181         """Toggle the status to Play/Pause.
 182         If no file is loaded, open the dialog window.
 183         """
 184         # check if there is a file to play, otherwise open a
 185         # Tk.FileDialog to select a file
 186         if not self.player.get_media():
 187             self.OnOpen()
 188         else:
 189             # Try to launch the media, if this fails display an error message
 190             if self.player.play() == -1:
 191                 self.errorDialog("Unable to play.")
 192 
 193     def GetHandle(self):
 194         return self.videopanel.winfo_id()
 195 
 196     #def OnPause(self, evt):
 197     def OnPause(self):
 198         """Pause the player.
 199         """
 200         self.player.pause()
 201 
 202     def OnStop(self):
 203         """Stop the player.
 204         """
 205         self.player.stop()
 206         # reset the time slider
 207         self.timeslider.set(0)
 208 
 209     def OnTimer(self):
 210         """Update the time slider according to the current movie time.
 211         """
 212         if self.player == None:
 213             return
 214         # since the self.player.get_length can change while playing,
 215         # re-set the timeslider to the correct range.
 216         length = self.player.get_length()
 217         dbl = length * 0.001
 218         self.timeslider.config(to=dbl)
 219 
 220         # update the time on the slider
 221         tyme = self.player.get_time()
 222         if tyme == -1:
 223             tyme = 0
 224         dbl = tyme * 0.001
 225         self.timeslider_last_val = ("%.0f" % dbl) + ".0"
 226         # don't want to programatically change slider while user is messing with it.
 227         # wait 2 seconds after user lets go of slider
 228         if time.time() > (self.timeslider_last_update + 2.0):
 229             self.timeslider.set(dbl)
 230 
 231     def scale_sel(self, evt):
 232         if self.player == None:
 233             return
 234         nval = self.scale_var.get()
 235         sval = str(nval)
 236         if self.timeslider_last_val != sval:
 237             # this is a hack. The timer updates the time slider.
 238             # This change causes this rtn (the 'slider has changed' rtn) to be invoked.
 239             # I can't tell the difference between when the user has manually moved the slider and when
 240             # the timer changed the slider. But when the user moves the slider tkinter only notifies
 241             # this rtn about once per second and when the slider has quit moving.
 242             # Also, the tkinter notification value has no fractional seconds.
 243             # The timer update rtn saves off the last update value (rounded to integer seconds) in timeslider_last_val
 244             # if the notification time (sval) is the same as the last saved time timeslider_last_val then
 245             # we know that this notification is due to the timer changing the slider.
 246             # otherwise the notification is due to the user changing the slider.
 247             # if the user is changing the slider then I have the timer routine wait for at least
 248             # 2 seconds before it starts updating the slider again (so the timer doesn't start fighting with the
 249             # user)
 250             self.timeslider_last_update = time.time()
 251             mval = "%.0f" % (nval * 1000)
 252             self.player.set_time(int(mval)) # expects milliseconds
 253 
 254 
 255     def volume_sel(self, evt):
 256         if self.player == None:
 257             return
 258         volume = self.volume_var.get()
 259         if volume > 100:
 260             volume = 100
 261         if self.player.audio_set_volume(volume) == -1:
 262             self.errorDialog("Failed to set volume")
 263 
 264 
 265 
 266     def OnToggleVolume(self, evt):
 267         """Mute/Unmute according to the audio button.
 268         """
 269         is_mute = self.player.audio_get_mute()
 270 
 271         self.player.audio_set_mute(not is_mute)
 272         # update the volume slider;
 273         # since vlc volume range is in [0, 200],
 274         # and our volume slider has range [0, 100], just divide by 2.
 275         self.volume_var.set(self.player.audio_get_volume())
 276 
 277     def OnSetVolume(self):
 278         """Set the volume according to the volume sider.
 279         """
 280         volume = self.volume_var.get()
 281         # vlc.MediaPlayer.audio_set_volume returns 0 if success, -1 otherwise
 282         if volume > 100:
 283             volume = 100
 284         if self.player.audio_set_volume(volume) == -1:
 285             self.errorDialog("Failed to set volume")
 286 
 287     def errorDialog(self, errormessage):
 288         """Display a simple error dialog.
 289         """
 290         Tk.tkMessageBox.showerror(self, 'Error', errormessage)
 291 
 292 def Tk_get_root():
 293     if not hasattr(Tk_get_root, "root"): #(1)
 294         Tk_get_root.root= Tk.Tk()  #initialization call is inside the function
 295     return Tk_get_root.root
 296 
 297 def _quit():
 298     print("_quit: bye")
 299     root = Tk_get_root()
 300     root.quit()     # stops mainloop
 301     root.destroy()  # this is necessary on Windows to prevent
 302                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate
 303     os._exit(1)
 304 
 305 if __name__ == "__main__":
 306     # Create a Tk.App(), which handles the windowing system event loop
 307     root = Tk_get_root()
 308     root.protocol("WM_DELETE_WINDOW", _quit)
 309 
 310     player = Player(root, title="tkinter vlc")
 311     # show the player window centred and run the application
 312     root.mainloop()
Python bindings for libvlcRSSAtom
