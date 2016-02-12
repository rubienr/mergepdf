#!/usr/bin/python

from Tkinter import *
from Tkinter import IntVar
import tkFileDialog
import tkMessageBox
from os.path import expanduser
from os import path
from os import makedirs
import subprocess

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
        self.rootWindow.resizable(True, False)
        self.rootWindow.title("Quick and Dirty PDF merging")
        self.defaultTextfieldWidth = 72

        self.isReverseDocumentBCheckboxValue = IntVar(False)
        self.isReverseDocumentB = False
        self.isReverseDocumentACheckboxValue = IntVar(False)
        self.isReverseDocumentA = False

        self.operationModeRadioButtonValue = StringVar()

        self.doOpenResultCheckboxValue = IntVar(False)
        self.doOpenResult = False
        
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

        reversedArgumentA=""
        if self.isReverseDocumentA:
            reversedArgumentA="end-1"

        reversedArgumentB=""
        if self.isReverseDocumentB:
            reversedArgumentB="end-1"

        self.actionEntry.insert(0, "pdftk A=%s B=%s %s A%s B%s output %s"
                                %(self.oddPdfEntry.get(),
                                  self.evenPdfEntry.get(),
                                  self.__getOperationMode(),
                                  reversedArgumentA,
                                  reversedArgumentB,
                                  self.outPdfEntry.get()))
        self.actionEntry.configure(state='readonly')

    # read state from shelve
    def __getIsReverseDocumentdA(self):
        if self.shelve.has_key("reverseA"):
            return self.shelve["reverseA"]
        else:
            return False

    # store state to shelve
    def __setIsReverseDocumentA(self, isReverseDocumentA):
        self.shelve["reverseA"] = isReverseDocumentA

    # read state from shelve
    def __getIsReverseDocumentdB(self):
        if self.shelve.has_key("reverseB"):
            return self.shelve["reverseB"]
        else:
            return False

    # store state to shelve
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

    # read state from shelve
    def __getDoOpenResult(self):
        if self.shelve.has_key("openResultAfterMerge"):
            return self.shelve["openResultAfterMerge"]
        else:
            return False

    # store state to shelve
    def __setDoOpenResult(self, doOpenResult):
        self.shelve["openResultAfterMerge"] = doOpenResult

    # read state from shelve
    def __getOperationMode(self):
        if self.shelve.has_key("operationMode"):
            return self.shelve["operationMode"]
        else:
            return "shuffle"

    # store state to shelve
    def __setOperationMode(self, operationMode):
        self.shelve["operationMode"] = operationMode

    def __quit(self):
        self.shelve.close()
        quit()

    def __initWindow(self):
        docAGroup = LabelFrame(self.rootWindow, text="Document containing odd sheets", padx=5, pady=5)
        #docAGroup.grid(row=2, column=0, columnspan=2)
        docAGroup.pack(padx=10, pady=10,fill='x')

        Button(docAGroup, text ="select document", command = self.__selectOddPages).grid(row=0, column=0,sticky=W)
        self.oddPdfEntry = Entry(docAGroup, width = self.defaultTextfieldWidth)
        self.oddPdfEntry.grid(row=0, column=1,sticky=W)

        isReversedeACheckBtn = Checkbutton(docAGroup, text="read document reversed", variable=self.isReverseDocumentACheckboxValue, command=self.__isReverseDocumentACheckboxCallback)
        isReversedeACheckBtn.grid(row=1, column=0, sticky=W)
        if self.__getIsReverseDocumentdA():
            isReversedeACheckBtn.select()


        docBGroup = LabelFrame(self.rootWindow, text="Document containing even sheets", padx=5, pady=5)
        #docBGroup.grid(row=2, column=0, columnspan=2)
        docBGroup.pack(padx=10, pady=10,fill='x')

        Button(docBGroup, text ="select document", command = self.__selectEvenPages, justify=LEFT).grid(row=0, column=0,sticky=W)
        self.evenPdfEntry =  Entry(docBGroup, width = self.defaultTextfieldWidth)
        self.evenPdfEntry.grid(row=0, column=1)

        isReversedBCheckBtn = Checkbutton(docBGroup, text="read document reversed", variable=self.isReverseDocumentBCheckboxValue, command=self.__isReverseDocumentBCheckboxCallback)
        isReversedBCheckBtn.grid(row=1, column=0)
        if self.__getIsReverseDocumentdB():
            isReversedBCheckBtn.select()


        outDdocGroup = LabelFrame(self.rootWindow, text="Output", padx=5, pady=5)
        #outDdocGroup.grid(row=2, column=0, columnspan=2)
        outDdocGroup.pack(padx=10, pady=10,fill='x')
        Button(outDdocGroup, text ="select otput folder", command = self.__selectOutDirectory).grid(row=0, column=0, sticky=W)
        self.outPdfEntry =  Entry(outDdocGroup, width = self.defaultTextfieldWidth)
        self.outPdfEntry.grid(row=0, column=1)
        self.outPdfEntry.insert(0, self.__getLastAccessedFolder() + "/merged.pdf")


        modeGroup = LabelFrame(self.rootWindow, text="Mode", padx=5, pady=5)
        modeGroup.pack(padx=10, pady=10, fill="x")
        modeRadio = Radiobutton(modeGroup, text="merge", variable=self.operationModeRadioButtonValue, value="shuffle", command=self.__modeChangedCallback)
        modeRadio.grid(row=0, column=0, sticky=W)
        modeRadio.config(state=NORMAL)
        modeRadio.select()
        modeRadio = Radiobutton(modeGroup, text="append", variable=self.operationModeRadioButtonValue, value="cat", command=self.__modeChangedCallback)
        modeRadio.grid(row=1, column=0, sticky=W)
        modeRadio.deselect()

        actionsGroup = LabelFrame(self.rootWindow, text="Merge", padx=5, pady=5)
        #actionsGroup .grid(row=2, column=0, columnspan=2)
        actionsGroup .pack(padx=10, pady=10,fill='x')
        actionBtn = Button(actionsGroup , text ="merge files", command = self.__shufflePdf)
        actionBtn.grid(row=0, column=0,sticky=W)
        #openDoc = Button(actionsGroup, text="view output", command=lambda : subprocess.call("xdg-open " + self.outPdfEntry.get(), shell=True))
        #openDoc.grid(row=0, column=1,sticky=W)
        doOpenOutput = Checkbutton(actionsGroup, text="open merged result", variable=self.doOpenResultCheckboxValue, command=self.__doOpenResultCheckboxCallback)
        doOpenOutput.grid(row=0, column=1, sticky=W)
        if self.__getDoOpenResult():
            doOpenOutput.select()


        actionLabel = Label(actionsGroup, text="applied command:")
        actionLabel.grid(row=1, column=0,sticky=W)
        self.actionEntry = Entry(actionsGroup , width = self.defaultTextfieldWidth)
        self.actionEntry.configure(state='readonly')
        self.actionEntry.grid(row=1, column=1)

        quitBtn = Button(self.rootWindow, text ="quit", command = self.__quit)
        quitBtn.pack()

    def __modeChangedCallback(self):
        self.__setOperationMode(self.operationModeRadioButtonValue.get())
        self.__updateAction()


    def __doOpenResultCheckboxCallback(self):
        value = False
        if self.doOpenResultCheckboxValue.get():
            value = True

        self.__setDoOpenResult(value)
        self.doOpenResult= value

    def __isReverseDocumentBCheckboxCallback(self):
        value = False
        if self.isReverseDocumentBCheckboxValue.get():
            value = True

        self.__setIsReverseDocumentB(value)
        self.isReverseDocumentB = value
        self.__updateAction()

    def __isReverseDocumentACheckboxCallback(self):
        value = False
        if self.isReverseDocumentACheckboxValue.get():
            value = True

        self.__setIsReverseDocumentA(value)
        self.isReverseDocumentA = value
        self.__updateAction()

    def __shufflePdf(self):
        self.__updateAction()
        status, output = commands.getstatusoutput(self.actionEntry.get())
        if not status == 0:
            print("status %s\noutput:\n%s" % (status, output))
            tkMessageBox.showinfo("Error", output)
        else:
            if self.__getDoOpenResult():
                subprocess.call("xdg-open " + self.outPdfEntry.get(), shell=True)

    def run(self):
        self.__initWindow()
        self.rootWindow.protocol("WM_DELETE_WINDOW", self.__quit)
        self.rootWindow.mainloop()

if __name__ == '__main__':
    taskPreparationGui = MergePdfGui()
    taskPreparationGui.run()
