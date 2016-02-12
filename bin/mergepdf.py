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
        self.isReverseDocumentACheckboxValue = IntVar(False)
        self.operationModeRadioButtonValue = StringVar()
        self.doOpenResultCheckboxValue = IntVar(False)
        
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

    def __onSelectEvenPagesCallback(self):
        self.openFileOptions["initialdir"] = self.__lastAccessedFolder()
        self.openFileOptions['title'] = "Select even pages"
        f = tkFileDialog.askopenfile(mode='r', **self.openFileOptions)
        self.evenPdfEntry.delete(0, END)
        self.evenPdfEntry.insert(0, f.name)
        self.__setLastAccessedFolder(path.dirname(f.name))
        self.__updateAction()
        return f

    def __onSelectOddPagesCallback(self):
        self.openFileOptions["initialdir"] = self.__lastAccessedFolder()
        self.openFileOptions['title'] = "Select odd pages"
        f = tkFileDialog.askopenfile(mode='r', **self.openFileOptions)
        self.oddPdfEntry.delete(0, END)
        self.oddPdfEntry.insert(0, f.name)
        self.__setLastAccessedFolder(path.dirname(f.name))
        self.__updateAction()
        return f

    def __onSelectOutDirectoryCallback(self):
        self.openDirectoryOptions["initialdir"] = self.__lastAccessedFolder()
        self.openDirectoryOptions['title'] = "Select output directory"
        f = tkFileDialog.askdirectory(**self.openDirectoryOptions)
        self.outPdfEntry.delete(0, END)
        self.outPdfEntry.insert(0, "%s/merged.pdf" % (f))
        self.__setLastAccessedFolder(f)
        self.__updateAction()
        return f

    def __updateAction(self):
        self.actionEntry.configure(state='normal')
        self.actionEntry.delete(0, END)

        reversedArgumentA=""
        if self.isReverseDocumentACheckboxValue.get():
            reversedArgumentA="end-1"

        reversedArgumentB=""
        if self.isReverseDocumentBCheckboxValue.get():
            reversedArgumentB="end-1"

        self.actionEntry.insert(0, "pdftk A=%s B=%s %s A%s B%s output %s"
                                %(self.oddPdfEntry.get(),
                                  self.evenPdfEntry.get(),
                                  self.__operationMode(),
                                  reversedArgumentA,
                                  reversedArgumentB,
                                  self.outPdfEntry.get()))
        self.actionEntry.configure(state='readonly')

    # read value from shelve
    def __readValueFromStore(self, index, defaultValue):
        if self.shelve.has_key(index):
            return self.shelve[index]
        else:
            return defaultValue

    # write value to shelve
    def __writeValueToStore(self, index, value):
        self.shelve[index] = value

    def __isReverseDocumentdA(self):
        return self.__readValueFromStore("reverseA", False)

    def __isReverseDocumentdB(self):
        return self.__readValueFromStore("reverseB", False)

    def __lastAccessedFolder(self):
        return self.__readValueFromStore("folder", "~")

    def __setLastAccessedFolder(self, folder):
        self.__writeValueToStore("folder", folder)

    # read state from shelve
    def __isOpenResultChecked(self):
        return self.__readValueFromStore("openResultAfterMerge", False)

    # read state from shelve
    def __operationMode(self):
            return self.__readValueFromStore("operationMode", "shuffle")

    def __onModeChangedCallback(self):
         self.__writeValueToStore("operationMode", self.operationModeRadioButtonValue.get())
         self.__updateAction()

    def __onDoOpenResultCheckboxCallback(self):
        value = False
        if self.doOpenResultCheckboxValue.get():
            value = True
        self.__writeValueToStore("openResultAfterMerge", value)

    def __onIsReverseDocumentBCheckboxCallback(self):
        value = False
        if self.isReverseDocumentBCheckboxValue.get():
            value = True
        self.__writeValueToStore("reverseB", value)
        self.__updateAction()

    def __onIsReverseDocumentACheckboxCallback(self):
        value = False
        if self.isReverseDocumentACheckboxValue.get():
            value = True
        self.__writeValueToStore("reverseA", value)
        self.__updateAction()


    def __quit(self):
        self.shelve.close()
        quit()

    def __initWindow(self):
        docAGroup = LabelFrame(self.rootWindow, text="Document containing odd sheets", padx=5, pady=5)
        docAGroup.pack(padx=10, pady=10,fill='x')
        Button(docAGroup, text ="select document", command = self.__onSelectOddPagesCallback).grid(row=0, column=0,sticky=W)
        self.oddPdfEntry = Entry(docAGroup, width = self.defaultTextfieldWidth)
        self.oddPdfEntry.grid(row=0, column=1,sticky=W)

        isReversedeACheckBtn = Checkbutton(docAGroup, text="read document reversed",
                                           variable=self.isReverseDocumentACheckboxValue,
                                           command=self.__onIsReverseDocumentACheckboxCallback)
        isReversedeACheckBtn.grid(row=1, column=0, sticky=W)
        if self.__isReverseDocumentdA():
            isReversedeACheckBtn.select()


        docBGroup = LabelFrame(self.rootWindow, text="Document containing even sheets", padx=5, pady=5)
        docBGroup.pack(padx=10, pady=10,fill='x')
        Button(docBGroup, text ="select document", command = self.__onSelectEvenPagesCallback, justify=LEFT).grid(row=0, column=0,sticky=W)
        self.evenPdfEntry =  Entry(docBGroup, width = self.defaultTextfieldWidth)
        self.evenPdfEntry.grid(row=0, column=1)

        isReversedBCheckBtn = Checkbutton(docBGroup, text="read document reversed",
                                          variable=self.isReverseDocumentBCheckboxValue,
                                          command=self.__onIsReverseDocumentBCheckboxCallback)
        isReversedBCheckBtn.grid(row=1, column=0)
        if self.__isReverseDocumentdB():
            isReversedBCheckBtn.select()


        outDdocGroup = LabelFrame(self.rootWindow, text="Output", padx=5, pady=5)
        outDdocGroup.pack(padx=10, pady=10,fill='x')
        Button(outDdocGroup, text ="select otput folder", command = self.__onSelectOutDirectoryCallback).grid(row=0, column=0, sticky=W)
        self.outPdfEntry =  Entry(outDdocGroup, width = self.defaultTextfieldWidth)
        self.outPdfEntry.grid(row=0, column=1)
        self.outPdfEntry.insert(0, self.__lastAccessedFolder() + "/merged.pdf")


        modeGroup = LabelFrame(self.rootWindow, text="Mode of operation", padx=5, pady=5)
        modeGroup.pack(padx=10, pady=10, fill="x")
        modeRadioBtn = Radiobutton(modeGroup, text="merge page by page", variable=self.operationModeRadioButtonValue, value="shuffle",
                                command=self.__onModeChangedCallback)
        modeRadioBtn.grid(row=0, column=0, sticky=W)
        if self.__operationMode() == "shuffle":
            modeRadioBtn.select()
        modeRadioBtn = Radiobutton(modeGroup, text="append 2nd document to 1st", variable=self.operationModeRadioButtonValue, value="cat",
                                command=self.__onModeChangedCallback)
        modeRadioBtn.grid(row=1, column=0, sticky=W)
        if self.__operationMode() == "cat":
            modeRadioBtn.select()


        actionsGroup = LabelFrame(self.rootWindow, text="Merge", padx=5, pady=5)
        actionsGroup .pack(padx=10, pady=10,fill='x')
        actionBtn = Button(actionsGroup , text ="merge files", command = self.__mergePdf)
        actionBtn.grid(row=0, column=0,sticky=W)
        doOpenOutput = Checkbutton(actionsGroup, text="open merged result", variable=self.doOpenResultCheckboxValue,
                                   command=self.__onDoOpenResultCheckboxCallback)
        doOpenOutput.grid(row=0, column=1, sticky=W)
        if self.__isOpenResultChecked():
            doOpenOutput.select()


        actionLabel = Label(actionsGroup, text="applied command:")
        actionLabel.grid(row=1, column=0,sticky=W)
        self.actionEntry = Entry(actionsGroup , width = self.defaultTextfieldWidth)
        self.actionEntry.configure(state='readonly')
        self.actionEntry.grid(row=1, column=1)


        quitBtn = Button(self.rootWindow, text ="quit", command = self.__quit)
        quitBtn.pack()


    def __mergePdf(self):
        self.__updateAction()
        status, output = commands.getstatusoutput(self.actionEntry.get())
        if not status == 0:
            print("status %s\noutput:\n%s" % (status, output))
            tkMessageBox.showinfo("Error", output)
        else:
            if self.__isOpenResultChecked():
                subprocess.call("xdg-open " + self.outPdfEntry.get(), shell=True)

    def run(self):
        self.__initWindow()
        self.rootWindow.protocol("WM_DELETE_WINDOW", self.__quit)
        self.rootWindow.mainloop()

if __name__ == '__main__':
    taskPreparationGui = MergePdfGui()
    taskPreparationGui.run()
