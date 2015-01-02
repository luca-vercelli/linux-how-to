#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Luca Vercelli 2014
#Released under GPL 2.0

import os
from Tkinter import *
#from gettext import gettext as _
import gettext
gettext.install("linuxHowTo")
import xdg2 as xdg
from shutil import copyfile

VERSION = "1.0"
BUTTON_HEIGHT = 70
BUTTON_WIDTH = 200
DESKTOP_FILENAME = "linuxHowTo.desktop"
MANUAL_FOLDER = xdg.HOME + "/.local/share/linuxHowTo/"
if not os.path.exists(MANUAL_FOLDER):
    MANUAL_FOLDER = "/usr/share/linuxHowTo/"
if not os.path.exists(MANUAL_FOLDER):
    print "Warning: manual pages not found!"


class App(Tk):
    """ call .mainloop() to launch """
    def __init__(self):
        Tk.__init__(self)
        self.initUI()
    def initUI(self):
        self.geometry("400x350+700+300")
        self.title(_("Linux HowTo"))
        self.mainframe = Frame(self)  #, background="gray"   
        self.mainframe.pack(fill=BOTH, expand=1)
        
        self.b1 = Button(self.mainframe, text=_("Browse internet"), command=xdg.browse_search_engine)
        self._place_button(self.b1, 0, 0)
        
        self.b4 = Button(self.mainframe, text=_("How to do what?"), command=self.manual_page)
        self._place_button(self.b4, 0, 1)
        
        self.b2 = Button(self.mainframe, text=_("Your videos"), command=xdg.open_videos)
        self._place_button(self.b2, 1, 0)
        
        self.b6 = Button(self.mainframe, text=_("Your music"), command=xdg.open_music)
        self._place_button(self.b6, 1, 0)
        
        self.b7 = Button(self.mainframe, text=_("Your images"), command=xdg.open_images)
        self._place_button(self.b7, 1, 0)
        
        self.b8 = Button(self.mainframe, text=_("Your downloads"), command=xdg.open_downloads)
        self._place_button(self.b8, 1, 0)
        
        self.b3 = Button(self.mainframe, text=_("Documents"), command=xdg.open_docs)
        self._place_button(self.b3, 1, 1)
        
        self.b5 = Button(self.mainframe, text=_("Word processing"), command=xdg.oowriter)
        self._place_button(self.b5, 2, 0)
        
        self.b2 = Button(self.mainframe, text=_("CD/DVD copy"), command=xdg.cd_dvd_copy)
        self._place_button(self.b2, 2, 1)
        
        self.chk = Checkbutton(self.mainframe, text=_("Open on startup"), command=self.switch_autostart)
        
        if os.path.exists(xdg.AUTOSTART_FOLDER + DESKTOP_FILENAME):
            self.chk.select()
            self.autostart = True
        else:
            self.chk.deselect()
            self.autostart = False
        
        self._place_button(self.chk, 3, 0)
        
        #self.lb = Listbox(self.mainframe)
        #for x in self.available_fractals:
        #    self.lb.insert(END, x)
        #self.lb.bind("<<ListboxSelect>>", self.onSelect)
        #self.lb.place(x=20, y=20)
        #self.status = StringVar()
        #self.label = Label(self.mainframe, textvariable=self.status)
        #self.label.place(x=20,y=180)
    def _place_button(self, but, i, j):
        """
        @param i = 0,1,2,...  y-coordinate
        @param j = 0,1  x-coordinate
        """
        but.place(x=BUTTON_WIDTH*j, y=BUTTON_HEIGHT*i, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
    def switch_autostart(self):
        if self.autostart:
            self.autostart = False
            autostart_disable()
        else:
            self.autostart = True
            autostart_enable()
    def manual_page(self, page="index.html"):
        xdg.browse(MANUAL_FOLDER + page)

def generate_docs():
    #We need localization...
    if not os.path.exists(MANUAL_FOLDER):
        print "Cannot find manual folder: '" + MANUAL_FOLDER + "'"
        return
    if not os.access(MANUAL_FOLDER, os.W_OK):
        print "Cannot write manual folder: '" + MANUAL_FOLDER + "'"
        return
    try:
        f = open(MANUAL_FOLDER + "inc.js", "w")
    except:
        print "IOError opening manual folder: '" + MANUAL_FOLDER + "'"
        return
        
    #LABELS
    f.write("var labels = new Array();\n")
    f.write("labels['title']='" + _("How to do what?") + "';\n") #translations must not contain "'"
    f.write("labels['application']='" + _("App") + "';\n")
    f.write("labels['filename']='" + _("Filename") + "';\n")
    f.write("labels['description']='" + _("Description") + "';\n")
    
    #APPLICATIONS
    #f.write("alert('DEBUG X');\n");
    apps = set()
    for mime in ['application/msword',  'application/msexcel','application/pdf', 'audio/mp3', 'audio/wav', 'video/mp4', 'application/x-zip', 'inode/directory']:
        desktop_file = xdg.get_desktop_file(mime)
        if not desktop_file is None:
            apps.add(desktop_file)
    app = xdg.find_browser()
    if app is not None:
        df = xdg.DesktopFile(app + ".desktop")
        if df.full_filename is not None:
            apps.add(df)
    app = xdg.find_email_client()
    if app is not None:
        df = xdg.DesktopFile(app + ".desktop")
        if df.full_filename is not None:
            apps.add(df)
    app = xdg.find_cd_dvd_burner()
    if app is not None:
        df = xdg.DesktopFile(app + ".desktop")
        if df.full_filename is not None:
            apps.add(df)
    app = xdg.find_music_player()
    if app is not None:
        df = xdg.DesktopFile(app + ".desktop")
        if df.full_filename is not None:
            apps.add(df)
    app = xdg.find_video_player()
    if app is not None:
        df = xdg.DesktopFile(app + ".desktop")
        if df.full_filename is not None:
            apps.add(df)
    app = xdg.find_explorer()
    if app is not None:
        df = xdg.DesktopFile(app + ".desktop")
        if df.full_filename is not None:
            apps.add(df)
    f.write("var app = new Array();\n")
    i = 0
    for desktop_file in sorted(apps,key=lambda df:df.name):
        _write_inc_item(i, desktop_file, f)
        i = i + 1
    #f.write("alert('DEBUG Y');\n");
    f.close()

def _write_inc_item(i, desktop_file, f):
            si = str(i)
            f.write("app[" + si + "] = new Object();\n")
            f.write("app[" + si + "].filename = '" + str(desktop_file.filename.replace(".desktop","")) + "';\n")
            f.write("app[" + si + "].name = '" + str(desktop_file.name) + "';\n")
            f.write("app[" + si + "].app = '" + str(desktop_file.app) + "';\n")
            f.write("app[" + si + "].generic_name = '" + str(desktop_file.generic_name) + "';\n")
            f.write("app[" + si + "].comment = '" + str(desktop_file.comment) + "';\n")
            f.write("app[" + si + "].icon = '" + str(desktop_file.icon) + "';\n")
            if desktop_file.icon_full_filename is not None:
                copyfile(desktop_file.icon_full_filename, MANUAL_FOLDER + desktop_file.icon)

def autostart_enable():
    """ Enable start on logon. This routine must work even if autostart was already enabled """
    os.system("mkdir -p " + xdg.AUTOSTART_FOLDER)
    for p in xdg.DESKTOP_FILE_PATHS:
        if os.path.exists(p + DESKTOP_FILENAME):
            from shutil import copyfile
            copyfile(p + DESKTOP_FILENAME, xdg.AUTOSTART_FOLDER + DESKTOP_FILENAME)
            break
            
def autostart_disable():
    """ Disable start on logon. This routine must work even if autostart was already disabled """
    p = xdg.AUTOSTART_FOLDER + DESKTOP_FILENAME
    if os.path.exists(p):
        os.remove(p)            
    
if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser(description="How-to manual for Linux beginners.", epilog="The program will automatically generate docs the first time it is run.")
    parser.add_argument('-v', '--version', action='store_true', help="show program version and exit")
    parser.add_argument('-g', '--generate', action='store_true', help="generate docs, then exit")
    parser.add_argument('--autostart_enable', action='store_true', help="enable autostart, then exit")
    parser.add_argument('--autostart_disable', action='store_true', help="disable autostart, then exit")
    args = parser.parse_args()
    
    if args.version:
        print sys.argv[0], VERSION
    elif args.generate:
        generate_docs()
    elif args.autostart_enable:
        autostart_enable()
    elif args.autostart_disable:
        autostart_disable()
    else:
        App().mainloop()


