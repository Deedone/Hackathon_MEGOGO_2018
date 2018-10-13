  #! /usr/bin/python
  # -*- coding: utf-8 -*-
  
  #
  # tkinter example for VLC Python bindings
  # Copyright (C) 2015 the VideoLAN team
  #
  # This program is free software; you can redistribute it and/or modify
  # it under the terms of the GNU General Public License as published by
  # the Free Software Foundation; either version 2 of the License, or
  # (at your option) any later version.
  #
  # This program is distributed in the hope that it will be useful,
  # but WITHOUT ANY WARRANTY; without even the implied warranty of
  # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  # GNU General Public License for more details.
  #
  # You should have received a copy of the GNU General Public License
  # along with this program; if not, write to the Free Software
  # Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
  #
  """A simple example for VLC python bindings using tkinter. Uses python 3.4
  
  Author: Patrick Fay
  Date: 23-09-2015
  """
  
  # import external libraries
  import vlc
  import sys
  
  if sys.version_info[0] < 3:
      import Tkinter as Tk
      from Tkinter import ttk
      from Tkinter.filedialog import askopenfilename
  else:
      import tkinter as Tk
      from tkinter import ttk
      from tkinter.filedialog import askopenfilename
  
  # import standard libraries
  import os
  import pathlib
  from threading import Thread, Event
  import time
  import platform
  
  class ttkTimer(Thread):
      """a class serving same function as wxTimer... but there may be better ways to do this
      """
      def __init__(self, callback, tick):
          Thread.__init__(self)
          self.callback = callback
          self.stopFlag = Event()
          self.tick = tick
          self.iters = 0
  
      def run(self):
          while not self.stopFlag.wait(self.tick):
              self.iters += 1
              self.callback()
  
      def stop(self):
          self.stopFlag.set()
  
      def get(self):
          return self.iters
  
  class Player(Tk.Frame):
      """The main window has to deal with events.
      """
      def __init__(self, parent, title=None):
          Tk.Frame.__init__(self, parent)
  
          self.parent = parent
  
          if title == None:
              title = "tk_vlc"
          self.parent.title(title)
  
          # Menu Bar
          #   File Menu
          menubar = Tk.Menu(self.parent)
          self.parent.config(menu=menubar)
  
          fileMenu = Tk.Menu(menubar)
          fileMenu.add_command(label="Open", underline=0, command=self.OnOpen)
          fileMenu.add_command(label="Exit", underline=1, command=_quit)
          menubar.add_cascade(label="File", menu=fileMenu)
  
          # The second panel holds controls
          self.player = None
          self.videopanel = ttk.Frame(self.parent)
          self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH,expand=1)
          self.videopanel.pack(fill=Tk.BOTH,expand=1)
  
          ctrlpanel = ttk.Frame(self.parent)
          pause  = ttk.Button(ctrlpanel, text="Pause", command=self.OnPause)
          play   = ttk.Button(ctrlpanel, text="Play", command=self.OnPlay)
 1        stop   = ttk.Button(ctrlpanel, text="Stop", command=self.OnStop)
 1        volume = ttk.Button(ctrlpanel, text="Volume", command=self.OnSetVolume)
 1        pause.pack(side=Tk.LEFT)
 1        play.pack(side=Tk.LEFT)
 1        stop.pack(side=Tk.LEFT)
 1        volume.pack(side=Tk.LEFT)
 1        self.volume_var = Tk.IntVar()
 1        self.volslider = Tk.Scale(ctrlpanel, variable=self.volume_var, command=self.volume_sel,
 1                from_=0, to=100, orient=Tk.HORIZONTAL, length=100)
 1        self.volslider.pack(side=Tk.LEFT)
 1        ctrlpanel.pack(side=Tk.BOTTOM)
 1
 1        ctrlpanel2 = ttk.Frame(self.parent)
 1        self.scale_var = Tk.DoubleVar()
 1        self.timeslider_last_val = ""
 1        self.timeslider = Tk.Scale(ctrlpanel2, variable=self.scale_var, command=self.scale_sel,
 1                from_=0, to=1000, orient=Tk.HORIZONTAL, length=500)
 1        self.timeslider.pack(side=Tk.BOTTOM, fill=Tk.X,expand=1)
 1        self.timeslider_last_update = time.time()
 1        ctrlpanel2.pack(side=Tk.BOTTOM,fill=Tk.X)
 1
 1
 1        # VLC player controls
 1        self.Instance = vlc.Instance()
 1        self.player = self.Instance.media_player_new()
 1
 1        # below is a test, now use the File->Open file menu
 1        #media = self.Instance.media_new('output.mp4')
 1        #self.player.set_media(media)
 1        #self.player.play() # hit the player button
 1        #self.player.video_set_deinterlace(str_to_bytes('yadif'))
 1
 1        self.timer = ttkTimer(self.OnTimer, 1.0)
 1        self.timer.start()
 1        self.parent.update()
 1
 1        #self.player.set_hwnd(self.GetHandle()) # for windows, OnOpen does does this
 1
 1
 1    def OnExit(self, evt):
 1        """Closes the window.
 1        """
 1        self.Close()
 1
 1    def OnOpen(self):
 1        """Pop up a new dialow window to choose a file, then play the selected file.
 1        """
 1        # if a file is already running, then stop it.
 1        self.OnStop()
 1
 1        # Create a file dialog opened in the current home directory, where
 1        # you can display all kind of files, having as title "Choose a file".
 1        p = pathlib.Path(os.path.expanduser("~"))
 1        fullname =  askopenfilename(initialdir = p, title = "choose your file",filetypes = (("all files","*.*"),("mp4 files","*.mp4")))
 1        if os.path.isfile(fullname):
 1            dirname  = os.path.dirname(fullname)
 1            filename = os.path.basename(fullname)
 1            # Creation
 1            self.Media = self.Instance.media_new(str(os.path.join(dirname, filename)))
 1            self.player.set_media(self.Media)
 1            # Report the title of the file chosen
 1            #title = self.player.get_title()
 1            #  if an error was encountred while retriving the title, then use
 1            #  filename
 1            #if title == -1:
 1            #    title = filename
 1            #self.SetTitle("%s - tkVLCplayer" % title)
 1
 1            # set the window id where to render VLC's video output
 1            if platform.system() == 'Windows':
 1                self.player.set_hwnd(self.GetHandle())
 1            else:
 1                self.player.set_xwindow(self.GetHandle()) # this line messes up windows
 1            # FIXME: this should be made cross-platform
 1            self.OnPlay()
 1
 1            # set the volume slider to the current volume
 1            #self.volslider.SetValue(self.player.audio_get_volume() / 2)
 1            self.volslider.set(self.player.audio_get_volume())
 1
 1    def OnPlay(self):
 1        """Toggle the status to Play/Pause.
 1        If no file is loaded, open the dialog window.
 1        """
 1        # check if there is a file to play, otherwise open a
 1        # Tk.FileDialog to select a file
 1        if not self.player.get_media():
 1            self.OnOpen()
 1        else:
 1            # Try to launch the media, if this fails display an error message
 1            if self.player.play() == -1:
 1                self.errorDialog("Unable to play.")
 1
 1    def GetHandle(self):
 1        return self.videopanel.winfo_id()
 1
 1    #def OnPause(self, evt):
 1    def OnPause(self):
 1        """Pause the player.
 1        """
 2        self.player.pause()
 2
 2    def OnStop(self):
 2        """Stop the player.
 2        """
 2        self.player.stop()
 2        # reset the time slider
 2        self.timeslider.set(0)
 2
 2    def OnTimer(self):
 2        """Update the time slider according to the current movie time.
 2        """
 2        if self.player == None:
 2            return
 2        # since the self.player.get_length can change while playing,
 2        # re-set the timeslider to the correct range.
 2        length = self.player.get_length()
 2        dbl = length * 0.001
 2        self.timeslider.config(to=dbl)
 2
 2        # update the time on the slider
 2        tyme = self.player.get_time()
 2        if tyme == -1:
 2            tyme = 0
 2        dbl = tyme * 0.001
 2        self.timeslider_last_val = ("%.0f" % dbl) + ".0"
 2        # don't want to programatically change slider while user is messing with it.
 2        # wait 2 seconds after user lets go of slider
 2        if time.time() > (self.timeslider_last_update + 2.0):
 2            self.timeslider.set(dbl)
 2
 2    def scale_sel(self, evt):
 2        if self.player == None:
 2            return
 2        nval = self.scale_var.get()
 2        sval = str(nval)
 2        if self.timeslider_last_val != sval:
 2            # this is a hack. The timer updates the time slider.
 2            # This change causes this rtn (the 'slider has changed' rtn) to be invoked.
 2            # I can't tell the difference between when the user has manually moved the slider and when
 2            # the timer changed the slider. But when the user moves the slider tkinter only notifies
 2            # this rtn about once per second and when the slider has quit moving.
 2            # Also, the tkinter notification value has no fractional seconds.
 2            # The timer update rtn saves off the last update value (rounded to integer seconds) in timeslider_last_val
 2            # if the notification time (sval) is the same as the last saved time timeslider_last_val then
 2            # we know that this notification is due to the timer changing the slider.
 2            # otherwise the notification is due to the user changing the slider.
 2            # if the user is changing the slider then I have the timer routine wait for at least
 2            # 2 seconds before it starts updating the slider again (so the timer doesn't start fighting with the
 2            # user)
 2            self.timeslider_last_update = time.time()
 2            mval = "%.0f" % (nval * 1000)
 2            self.player.set_time(int(mval)) # expects milliseconds
 2
 2
 2    def volume_sel(self, evt):
 2        if self.player == None:
 2            return
 2        volume = self.volume_var.get()
 2        if volume > 100:
 2            volume = 100
 2        if self.player.audio_set_volume(volume) == -1:
 2            self.errorDialog("Failed to set volume")
 2
 2
 2
 2    def OnToggleVolume(self, evt):
 2        """Mute/Unmute according to the audio button.
 2        """
 2        is_mute = self.player.audio_get_mute()
 2
 2        self.player.audio_set_mute(not is_mute)
 2        # update the volume slider;
 2        # since vlc volume range is in [0, 200],
 2        # and our volume slider has range [0, 100], just divide by 2.
 2        self.volume_var.set(self.player.audio_get_volume())
 2
 2    def OnSetVolume(self):
 2        """Set the volume according to the volume sider.
 2        """
 2        volume = self.volume_var.get()
 2        # vlc.MediaPlayer.audio_set_volume returns 0 if success, -1 otherwise
 2        if volume > 100:
 2            volume = 100
 2        if self.player.audio_set_volume(volume) == -1:
 2            self.errorDialog("Failed to set volume")
 2
 2    def errorDialog(self, errormessage):
 2        """Display a simple error dialog.
 2        """
 2        Tk.tkMessageBox.showerror(self, 'Error', errormessage)
 2
 2def Tk_get_root():
 2    if not hasattr(Tk_get_root, "root"): #(1)
 2        Tk_get_root.root= Tk.Tk()  #initialization call is inside the function
 2    return Tk_get_root.root
 2
 2def _quit():
 2    print("_quit: bye")
 2    root = Tk_get_root()
 3    root.quit()     # stops mainloop
 3    root.destroy()  # this is necessary on Windows to prevent
 3                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
 3    os._exit(1)
 3
 3if __name__ == "__main__":
 3    # Create a Tk.App(), which handles the windowing system event loop
 3    root = Tk_get_root()
 3    root.protocol("WM_DELETE_WINDOW", _quit)
 3
 3    player = Player(root, title="tkinter vlc")
 3    # show the player window centred and run the application
 3    root.mainloop()
Pyn bindings for libvlcRSSAt