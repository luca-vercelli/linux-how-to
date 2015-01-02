#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Luca Vercelli 2014
#Released under GPL
#
#I don't trust in xdg module yet ...

import os, subprocess, re, locale

def _getfullout(linux_command):
    """ return stdout of subprocess """
    out = subprocess.Popen(linux_command, shell=True, stdout=subprocess.PIPE).communicate()[0]
    return out.split('\n')
def _getout(linux_command):
    """ return first line of stdout of subprocess """
    out = _getfullout(linux_command)
    if out:
        return out[0]
    else:
        return ""
    
HOME = os.path.expanduser('~')
USERNAME = _getout("id -un")
ETC_ISSUE = _getout("cat /etc/issue")
AUTOSTART_FOLDER = HOME + "/.config/autostart/"
DESKTOP_FILE_PATHS = [HOME + '/.local/share/applications/', '/usr/share/applications/']
(LANG, ENC) = locale.getlocale() #FIXME why it's always None ?
if LANG is None:
    (LANG, ENC) = locale.getdefaultlocale()
LANG_SHORT = None
if LANG is not None:
    LANG_SHORT = (LANG + "_" ).split("_")[0]
    
def browse(url): 
    os.system("xdg-open '" + url + "'")
def browse_search_engine(query=None):
    #FIXME ...
    if query is None:
        browse("http://www.duckduckgo.com")
    else:
        browse("http://www.duckduckgo.com?q="+query)

def open_doc(path):
    os.system("xdg-open '" + path + "'")
    
def write_email():
    os.system("xdg-mail")
    
def screensaver_activate():
    os.system("xdg-screensaver activate")
def screensaver_lock():
    os.system("xdg-screensaver lock")
    
def get_user_folder(uf):
    """
    @param uf user folder, as accepted by xdg-user-dir
    """
    return _getout("xdg-user-dir " + uf)
    
def open_user_folder(uf):
    """
    @param uf user folder, as accepted by xdg-user-dir
    """
    os.system("xdg-open `xdg-user-dir " + uf + "`")
def open_docs(): 
    open_user_folder("DOCUMENTS")
def open_videos(): 
    open_user_folder("VIDEOS")
def open_images(): 
    open_user_folder("PICTURES")
def open_music(): 
    open_user_folder("MUSIC")
def open_downloads(): 
    open_user_folder("DOWNLOAD")

class DesktopFile():
    def __init__(self, filename):
        self.filename = filename
        self.full_filename = None
        self.app = None
        self.name = None
        self.generic_name = None
        self.comment = None
        self.type = None
        self.icon = None
        self.icon_full_filename = None
        self.categories = []
        self.mime_types = []
        if filename is None or filename.strip() == "":
            return
        for p in DESKTOP_FILE_PATHS:
            if os.path.exists(p+filename):
                self.full_filename = p+filename
                break
        if self.full_filename is None:
            return
        with open(self.full_filename) as f:
            content = f.readlines()
        
        skip_section = False
        for line in content:
            section = re.match(r'^\[(.+?)\]$', line)
            if section is not None:  #We just consider de
                skip_section = ( section.group(1).strip().lower() != "desktop entry" )
                continue
            if skip_section:
                continue
            
            groups = re.search(r'^\s*(.+?)(\[(.*)\])?\s*=\s*(.+?)\s*$', line)
            if groups is None:
                continue
            #I hope all implementations behaves in this way...
            left_side = groups.group(1)
            lang = groups.group(3)
            right_side = groups.group(4)
            
            if left_side is None:
                continue
            left_side = left_side.strip().lower()
            if lang is not None and lang != LANG and lang != LANG_SHORT:
                continue
                
            if left_side == "exec":
                self.app = right_side
            elif left_side == "icon":
                self.icon = right_side
                #FIXME how to get full filename? and theme?
            elif left_side == "name":
                if lang is not None or self.name is None:
                    self.name = right_side
            elif left_side == "genericname":
                if lang is not None or self.generic_name is None:
                    self.generic_name = right_side
            elif left_side == "comment":
                if lang is not None or self.comment is None:
                    self.comment = right_side
            elif left_side == "categories":
                self.categories = right_side.split(';')
            elif left_side == "mimetype":
                self.mime_types = right_side.split(';')
        if self.icon is not None:
            self.icon_full_filename = self.get_icon_full_filename()

    def get_icon_full_filename(self):
        """
        We search *one* of the existing icons with given name 
        What's the rule for getting the right one ???
        """ #FIXME
        filename = self.icon + ".png"
        for theme in ['Mint-X','gnome','hicolor']:
            t = _getout("find /usr/share/icons -iname '"+filename+"' | grep '"+theme+"' | grep 48")
            if t != "":
                return t
        t = _getout("find /usr/share/icons -iname '"+filename+"' | grep 48")
        if t != "":
            return t
        filename = self.icon + ".svg"
        for theme in ['gnome','Mint-X','hicolor']:
            t = _getout("find /usr/share/icons -iname '"+filename+"' | grep '"+theme+"' ")
            if t != "":
                return t
        t = _getout("find /usr/share/icons -iname '"+filename+"'")
        if t != "":
            return t
        return None
        
    def __str__(self):
        return "Desktop file "  + self.filename
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.filename == other.filename)
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash(self.filename)
        
def get_desktop_file(mime_type):
    """ Return the DesktopFile of the default application for given MIME type """
    desktop_file = _getout("xdg-mime query default " + mime_type)
    if desktop_file is not None and desktop_file.strip() != "":
        return DesktopFile(desktop_file)
    else:
        return None

def get_mime_filetype(path):
    """ Return the name of the MIME type for a given file """
    return _getout("xdg-mime query filetype " + path)

def launch_default_app(mime_type):
    desktopfile = get_desktop_file(mime_type)
    if desktopfile is not None and desktopfile.app != None and desktopfile.app != "":
        app = str(desktopfile.app).replace("%U","") #FIXME what is %U ???
        os.system(app)

def oowriter():
    launch_default_app("application/msword")

def oocalc():
    launch_default_app("application/msexcel")

def get_default_browser():
    desktop_file = _getout("xdg-settings get default-web-browser")
    if desktop_file is not None and desktop_file.strip() != "":
        return DesktopFile(desktop_file)
    else:
        return None

def program_is_installed(binary_name):
    path = _getout("whereis " + binary_name + "|cut -d\":\" -f2|cut -d\" \" -f2")
    if path is None or path.strip() == "":
        return False
    return True
    
def _find_programs(programs,just_one=True):
    """
    Return the program/the programs, in the given list, that are installed 
    @param programs list of strings, which are the names of the binaries to be searched for
    @just_one if True, return just the first program, or None; if False, return the list of all programs
    @return string or list of strings, according to just_one
    """
    if just_one:
        for p in programs:
            if program_is_installed(p):
                return p
        return None
    else:
        ret = []
        for p in programs:
            if program_is_installed(p):
                ret.append(p)

def find_email_client(just_one=True):
    programs = ["thunderbird","kmail","evolution","seamonkey","zimbra"]
    return _find_programs(programs,just_one)

def find_browser(just_one=True):
    programs = ["firefox","chromium","google-chrome","konqueror","rekonq","opera","midori","icecat","epiphany"]
    return _find_programs(programs,just_one)

def find_cd_dvd_burner(just_one=True):
    programs = ["brasero","k3b"]
    return _find_programs(programs,just_one)

def find_music_player(just_one=True):
    programs = ["banshee","rythmbox","songbird","amarok","audacious","atunes","mplayer"]
    return _find_programs(programs,just_one)

def find_video_player(just_one=True):
    programs = ["totem", "kaffeine","vlc", "miro", "boxee"]
    return _find_programs(programs,just_one)

def find_explorer(just_one=True):
    programs = ["dolphin", "d3lphin","nautilus", "nemo"]
    return _find_programs(programs,just_one)

def cd_dvd_copy():
    #launch_default_app("application/x-cd-image")#FIXME don't work
    pgm = find_cd_dvd_burner()
    if pgm is not None:
        os.system(pgm)
    else:
        print "No program found for CD-DVD burning"

if __name__ == "__main__":      #Just for debug, or for demo
    print "Username:", USERNAME
    print "HOME:", HOME
    print "LANG:", LANG, LANG_SHORT
    print "ENC:", ENC
    print "/etc/issue:", ETC_ISSUE
    print "Documents folder:", get_user_folder("DOCUMENTS")
    print "What kind of OpenOffice Writer:", get_desktop_file("application/msword").app
    print "What kind of OpenOffice Calc:", get_desktop_file("application/msexcel").app
    print "OpenOffice Writer is registered under categories:", get_desktop_file("application/msword").categories
    print "Default browser:", get_default_browser().name
    
