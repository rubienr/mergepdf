#!/usr/bin/python

from Tkinter import *
import tkFileDialog
from os.path import expanduser
from os import system as sys

home = expanduser("~")
top = Tk()

options = {}
options['defaultextension'] = '.pdf'
options['filetypes'] = [('PDF', '.pdf')]
options['initialdir'] = home
options['initialfile'] = ''
options['parent'] = top
options['title'] = 'Select %s files'

dirOptions = {}
dirOptions['initialdir'] = home
dirOptions['mustexist'] = 'true'
dirOptions['parent'] = top
dirOptions['title'] = '"Select output directory"'

  
def selectEvenPages():
    options['title'] = "Select even pages"
    f = tkFileDialog.askopenfile(mode='r', **options)
    evenEntry.delete(0, END)
    evenEntry.insert(0, f.name)
    updateAction()
    return f

def selectOddPages():
    options['title'] = "Select odd pages"
    f = tkFileDialog.askopenfile(mode='r', **options )
    oddEntry.delete(0, END)
    oddEntry.insert(0, f.name)
    updateAction()
    return f

def selectOutDirectory():
    options['title'] = "Select output directory"
    f = tkFileDialog.askdirectory(**dirOptions)
    outEntry.delete(0, END)
    print("f: %s" %(f))
    outEntry.insert(0, "%s/xxx.pdf" % (f))
    return f

def updateAction():
    actionEntry.delete(0, END)
    actionEntry.insert(0, "pdftk A=%s B=%s shuffle A B output %s" %(oddEntry.get(), evenEntry.get(), outEntry.get()))

def shufflePdf():
    updateAction()
    print("calling: %s" %(actionEntry.get()))
    sys(actionEntry.get())

defaultTextWidth = 100

oddpdf = Button(top, text ="odd file", command = selectOddPages)
oddpdf.pack()
oddLabel = Label(top, text="Odd file:")
oddLabel.pack()
oddEntry =  Entry(top, width = defaultTextWidth)
oddEntry.pack()

evenpdf = Button(top, text ="even file", command = selectEvenPages, justify=LEFT)
evenpdf.pack()
evenLabel = Label(top, text="Even file:")
evenLabel.pack()
evenEntry =  Entry(top, width = defaultTextWidth)
evenEntry.pack()

outDir = Button(top, text ="outputDirectory", command = selectOutDirectory)
outDir.pack()
outLabel = Label(top, text="output *.pdf:")
outLabel.pack()
outEntry =  Entry(top, width = defaultTextWidth)
outEntry.pack()
outEntry.pack()
outEntry.delete(0, END)
outEntry.insert(0, "~/xxx.pdf" )

actionBt = Button(top, text ="merge", command = shufflePdf)
actionBt.pack()
actionLabel = Label(top, text="last command:")
actionLabel.pack()
actionEntry = Entry(top, width = defaultTextWidth)
actionEntry.pack()


quitBtn = Button(top, text ="quit", command = quit)
quitBtn.pack()


top.mainloop()
