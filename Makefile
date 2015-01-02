DESTDIR ?= 
BINDIR ?= /usr/bin
MANDIR ?= /usr/share/linuxHowTo

all:
	mkdir -p build/mo
	msgfmt po/it.po -o build/mo/it.mo

install: all
	mkdir -p $(DESTDIR)$(BINDIR)
	cp linuxHowTo.py $(DESTDIR)$(BINDIR)/linuxHowTo 2>/dev/null || :       #non recursive!
	chmod a+x $(DESTDIR)$(BINDIR)/linuxHowTo
	#pyshared.
	mkdir -p $(DESTDIR)/usr/share/pyshared
	cp xdg2.py $(DESTDIR)/usr/share/pyshared/xdg2.py
	#python modules symlinks
	mkdir -p $(DESTDIR)/usr/lib/python2.5/
	mkdir -p $(DESTDIR)/usr/lib/python2.6/
	mkdir -p $(DESTDIR)/usr/lib/python2.7/
	ln -sf /usr/share/pyshared/xdg2.py $(DESTDIR)/usr/lib/python2.5/
	ln -sf /usr/share/pyshared/xdg2.py $(DESTDIR)/usr/lib/python2.6/
	ln -sf /usr/share/pyshared/xdg2.py $(DESTDIR)/usr/lib/python2.7/
	#launch icon
	mkdir -p $(DESTDIR)/usr/share/applications/
	cp linuxHowTo.desktop $(DESTDIR)/usr/share/applications/
	#html stuff
	mkdir -p $(DESTDIR)/usr/share/linuxHowTo
	cp html/* $(DESTDIR)/usr/share/linuxHowTo
	#locales
	#FIXME: is there a more clever way?
	mkdir -p $(DESTDIR)/usr/share/locale/it/LC_MESSAGES
	cp build/mo/it.mo $(DESTDIR)/usr/share/locale/it/LC_MESSAGES/linuxHowTo.mo
	#generate docs
	#For building a Debian package this should be put in postinst script, or in config
	linuxHowTo --generate
        
localinstall:
	#FIXME what's the best way of doing a non-root install?
	mkdir -p ~/bin
	cp linuxHowTo.py ~/bin/linuxHowTo 2>/dev/null || :       #non recursive!
	chmod a+x ~/bin/linuxHowTo
	#pyshared.
	mkdir -p ~/.local/share/pyshared
	cp xdg2.py ~/.local/share/pyshared/xdg2.py
	#python modules symlinks
	mkdir -p ~/.local/lib/python2.5/
	mkdir -p ~/.local/lib/python2.6/
	mkdir -p ~/.local/lib/python2.7/
	ln -sf ~/.local/share/pyshared/xdg2.py ~/.local/lib/python2.5/
	ln -sf ~/.local/share/pyshared/xdg2.py ~/.local/lib/python2.6/
	ln -sf ~/.local/share/pyshared/xdg2.py ~/.local/lib/python2.7/
	#launch icon
	mkdir -p ~/.local/share/applications/
	cp linuxHowTo.desktop ~/.local/share/applications/
	#html stuff
	mkdir -p ~/.local/share/linuxHowTo
	cp html/* ~/.local/share/linuxHowTo
	#locales
	cp build/mo/it.mo ~/.local/share/locale/it/LC_MESSAGES/linuxHowTo.mo
        
uninstall:
	rm -rf $(DESTDIR)$(MANDIR)
	rm -f $(DESTDIR)/usr/share/pyshared/xdg2.py
	rm -f $(DESTDIR)/usr/lib/python2.*/xdg2.py
	rm -f $(DESTDIR)/usr/share/applications/linuxHowTo.desktop
	rm -f $(DESTDIR)$(BINDIR)/linuxHowTo
	rm -f $(DESTDIR)/usr/share/locale/*/LC_MESSAGES/linuxHowTo.mo
	

