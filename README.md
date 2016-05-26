# mergepdf
Quick and dirty PDF merging GUI. Merges single sided scans. Usefull if your scanner does not support double sided scanning.
+ merge side by side or
+ append document

![merge process illustration](https://rawgithub.com/rubienr/mergepdf/master/docs/merge-illustration.svg)

# Usage
Clone repository:
```
    git pull https://github.com/rubienr/mergepdf.git
```
Start GUI:
```
    cd mergepdf
    bin/mergepdf.sh
```
[Merge:](https://github.com/rubienr/mergepdf/blob/master/docs/gui.jpg)
<ol>
<li>select document containing odd files</li>
<li>select document containing even files</li>
<li>select destination folder/file-name</li>
<li>press merge button</li>
</ol>
# Needed Tools
+ python2
+ pypy-tk
+ python-tk
+ pdftk

Ubuntu:
```
    sudo apt-get install python2 pypy-tk python-tk pdftk
```
# Screenshots

![gui](https://raw.githubusercontent.com/rubienr/mergepdf/master/docs/gui.jpg)
