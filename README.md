linux-how-to
============

Application for helping Linux beginners.

Its intended use is to be installed in laptops where Linux is pre-installed.

Build translations files with

```
make
```

(currently, only Italian is provided).
Then install with:

```
sudo make install
```

and run from command line with

```
linuxHowTo
```

Instead of using make, you can also create Debian package with

```
dpkg-buildpackage
```
  
and then install the .deb package.



