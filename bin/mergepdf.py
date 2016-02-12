#!/usr/bin/python

from Tkinter import *
from Tkinter import IntVar
import tkFileDialog
import tkMessageBox
from os.path import expanduser
from os import path
from os import makedirs
from os import system as sys
import shelve
import commands

class MergePdfGui:
    def __init__(self):
        self.shelveDirectory = path.dirname(__file__)
        self.shelveFileName = "settings.shelve"
        if not path.exists(self.shelveDirectory):
            makedirs(self.shelveDirectory)
        self.shelve = shelve.open(self.shelveDirectory + "/" + self.shelveFileName)

        self.homeDirectory = expanduser("~")
        self.rootWindow = Tk()
        self.rootWindow.title("Quick and Dirty PDF merging")
        self.defaultTextfieldWidth = 100

        self.isReverseDocumentBCheckboxValue = IntVar(False)
        self.isReverseDocumentB = False
        
        self.openFileOptions = {}
        self.openFileOptions['defaultextension'] = '.pdf'
        self.openFileOptions['filetypes'] = [('PDF', '.pdf')]
        self.openFileOptions['initialdir'] = self.homeDirectory
        self.openFileOptions['initialfile'] = ''
        self.openFileOptions['parent'] = self.rootWindow
        self.openFileOptions['multiple'] = "false"
        self.openFileOptions['title'] = 'Select %s files'

        self.openDirectoryOptions = {}
        self.openDirectoryOptions['initialdir'] = self.homeDirectory
        self.openDirectoryOptions['mustexist'] = 'true'
        self.openDirectoryOptions['parent'] = self.rootWindow
        self.openDirectoryOptions['title'] = '"Select output directory"'

    def __selectEvenPages(self):
        self.openFileOptions["initialdir"] = self.__getLastAccessedFolder()
        self.openFileOptions['title'] = "Select even pages"
        f = tkFileDialog.askopenfile(mode='r', **self.openFileOptions)
        self.evenPdfEntry.delete(0, END)
        self.evenPdfEntry.insert(0, f.name)
        self.__updateAction()
        self.__setLastAccessedFolder(path.dirname(f.name))
        return f

    def __selectOddPages(self):
        self.openFileOptions["initialdir"] = self.__getLastAccessedFolder()
        self.openFileOptions['title'] = "Select odd pages"
        f = tkFileDialog.askopenfile(mode='r', **self.openFileOptions)
        self.oddPdfEntry.delete(0, END)
        self.oddPdfEntry.insert(0, f.name)
        self.__updateAction()
        self.__setLastAccessedFolder(path.dirname(f.name))
        return f

    def __selectOutDirectory(self):
        self.openDirectoryOptions["initialdir"] = self.__getLastAccessedFolder()
        self.openDirectoryOptions['title'] = "Select output directory"
        f = tkFileDialog.askdirectory(**self.openDirectoryOptions)
        self.outPdfEntry.delete(0, END)
        self.outPdfEntry.insert(0, "%s/merged.pdf" % (f))
        self.__setLastAccessedFolder(f)
        return f

    def __updateAction(self):
        self.actionEntry.configure(state='normal')
        self.actionEntry.delete(0, END)
        #self.actionEntry.insert(0, "pdftk A=%s B=%s shuffle A B output %s" %(self.oddPdfEntry.get(), self.evenPdfEntry.get(), self.outPdfEntry.get()))

        reversedArgument=""
        if self.isReverseDocumentB:
            reversedArgument="end-1"

        self.actionEntry.insert(0, "pdftk A=%s B=%s shuffle A B%s output %s" %(self.oddPdfEntry.get(), self.evenPdfEntry.get(), reversedArgument, self.outPdfEntry.get()))
        self.actionEntry.configure(state='readonly')

    # store state to shelve
    def __getIsReverseDocumentdB(self):
        if self.shelve.has_key("reverseB"):
            return self.shelve["reverseB"]
        else:
            return False

    # read state from shelve
    def __setIsReverseDocumentB(self, isReverseDocumentB):
        self.shelve["reverseB"] = isReverseDocumentB

    # read state from shelve
    def __getLastAccessedFolder(self):
        if self.shelve.has_key("folder"):
            return self.shelve["folder"]
        else:
            return "~"

    # store state to shelve
    def __setLastAccessedFolder(self, folder):
        self.shelve["folder"] = folder

    def __quit(self):
        self.shelve.close()
        quit()

    def __initWindow(self):
        oddPdfBtn = Button(self.rootWindow, text ="select odd sheets", command = self.__selectOddPages)
        oddPdfBtn.pack()
        oddPdfLabel = Label(self.rootWindow, text="Odd file:")
        oddPdfLabel.pack()
        self.oddPdfEntry =  Entry(self.rootWindow, width = self.defaultTextfieldWidth)
        self.oddPdfEntry.pack()
        
        evenPdfBtn = Button(self.rootWindow, text ="select even sheets", command = self.__selectEvenPages, justify=LEFT)
        evenPdfBtn.pack()
        evenPdfLabel = Label(self.rootWindow, text="Even file:")
        evenPdfLabel.pack()
        self.evenPdfEntry =  Entry(self.rootWindow, width = self.defaultTextfieldWidth)
        self.evenPdfEntry.pack()
        
        outDirBtn = Button(self.rootWindow, text ="select otput folder", command = self.__selectOutDirectory)
        outDirBtn.pack()
        outDirLabel = Label(self.rootWindow, text="Merged output *.pdf:")
        outDirLabel.pack()
        self.outPdfEntry =  Entry(self.rootWindow, width = self.defaultTextfieldWidth)
        self.outPdfEntry.pack()
        self.outPdfEntry.insert(0, self.__getLastAccessedFolder() + "/merged.pdf")

        checkBtn = Checkbutton(self.rootWindow, text="Reverse even pages document", variable=self.isReverseDocumentBCheckboxValue, command=self.__isReverseDocumentBCheckboxCallback)
        if self.__getIsReverseDocumentdB():
            checkBtn.select()
        checkBtn.pack()

        actionBtn = Button(self.rootWindow, text ="merge files", command = self.__shufflePdf)
        actionBtn.pack()
        actionLabel = Label(self.rootWindow, text="Applied command:")
        actionLabel.pack()

        self.actionEntry = Entry(self.rootWindow, width = self.defaultTextfieldWidth)
        self.actionEntry.configure(state='readonly')
        self.actionEntry.pack()
        
        quitBtn = Button(self.rootWindow, text ="quit", command = self.__quit)
        quitBtn.pack()

    def __isReverseDocumentBCheckboxCallback(self):
        if self.isReverseDocumentBCheckboxValue.get():
            self.__setIsReverseDocumentB(True)
            self.isReverseDocumentB = True
        else:
            self.__setIsReverseDocumentB(False)
            self.isReverseDocumentB = False

    def __shufflePdf(self):
        self.__updateAction()
        status, output = commands.getstatusoutput(self.actionEntry.get())
        if not status == 0:
            print("status %s\noutput:\n%s" % (status, output))
            tkMessageBox.showinfo("Error", output)

    def run(self):
        self.__initWindow()
        self.rootWindow.protocol("WM_DELETE_WINDOW", self.__quit)
        self.rootWindow.mainloop()

if __name__ == '__main__':
    taskPreparationGui = MergePdfGui()
    taskPreparationGui.run()
