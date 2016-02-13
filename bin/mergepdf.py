#!/usr/bin/python
#
# @author rubienr 2/2016
#
from Tkinter import *
from Tkinter import IntVar
import tkFileDialog
import tkMessageBox
from os.path import expanduser
from os import path
from os import makedirs
import subprocess
import shelve
from Pdftk import Pdftk
from UpdateCheck import UpdateCheck
from threading import Thread
import time

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

        self.pdftk = Pdftk()
        self.updateAvailable = False
        self.run()

    def __onSelectEvenPagesCallback(self):
        self.openFileOptions["initialdir"] = self.__lastAccessedFolder()
        self.openFileOptions['title'] = "Select even pages"
        f = tkFileDialog.askopenfile(mode='r', **self.openFileOptions)
        if f:
            self.evenPdfEntry.delete(0, END)
            self.evenPdfEntry.insert(0, f.name)
            self.__setLastAccessedFolder(path.dirname(f.name))
            self.__updateAction()
        return f

    def __onSelectOddPagesCallback(self):
        self.openFileOptions["initialdir"] = self.__lastAccessedFolder()
        self.openFileOptions['title'] = "Select odd pages"
        f = tkFileDialog.askopenfile(mode='r', **self.openFileOptions)
        if f:
            self.oddPdfEntry.delete(0, END)
            self.oddPdfEntry.insert(0, f.name)
            self.__setLastAccessedFolder(path.dirname(f.name))
            self.__updateAction()
        return f

    def __onSelectOutDirectoryCallback(self):
        self.openDirectoryOptions["initialdir"] = self.__lastAccessedFolder()
        self.openDirectoryOptions['title'] = "Select output directory"
        f = tkFileDialog.askdirectory(**self.openDirectoryOptions)
        if f:
            self.outPdfEntry.delete(0, END)
            self.outPdfEntry.insert(0, "%s/merged.pdf" % (f))
            self.__setLastAccessedFolder(f)
            self.__updateAction()
        return f

    def __updateAction(self):
        self.actionEntry.configure(state='normal')
        self.actionEntry.delete(0, END)

        reversedArgumentA = "normal"
        if self.isReverseDocumentACheckboxValue.get():
            reversedArgumentA = "reversed"

        reversedArgumentB = "normal"
        if self.isReverseDocumentBCheckboxValue.get():
            reversedArgumentB = "reversed"

        self.pdftk.update(documentA=self.oddPdfEntry.get(), documentB=self.evenPdfEntry.get(), documentAOrder=reversedArgumentA,
                          documentBOrder=reversedArgumentB, outputDocument=self.outPdfEntry.get(), operationMode=self.__operationMode())
        self.actionEntry.insert(0, self.pdftk.getCommandString())
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
        return self.__readValueFromStore("operationMode", "merge")

    def __onModeChangedCallback(self):
        self.__writeValueToStore("operationMode", self.operationModeRadioButtonValue.get())
        self.__updateAction()
        self.__updateDocumentIllustration()

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
        self.__updateDocumentIllustration()

    def __onIsReverseDocumentACheckboxCallback(self):
        value = False
        if self.isReverseDocumentACheckboxValue.get():
            value = True
        self.__writeValueToStore("reverseA", value)
        self.__updateAction()
        self.__updateDocumentIllustration()

    def __updateDocumentIllustration(self):
        if self.operationModeRadioButtonValue.get() == "merge":
            if self.isReverseDocumentACheckboxValue.get():
                self.documentSides["A1"].grid(column = self.documentSidesGridColumnIndex[4])
                self.documentSides["A2"].grid(column = self.documentSidesGridColumnIndex[2])
                self.documentSides["A3"].grid(column = self.documentSidesGridColumnIndex[0])
            else:
                self.documentSides["A1"].grid(column = self.documentSidesGridColumnIndex[0])
                self.documentSides["A2"].grid(column = self.documentSidesGridColumnIndex[2])
                self.documentSides["A3"].grid(column = self.documentSidesGridColumnIndex[4])
            if self.isReverseDocumentBCheckboxValue.get():
                self.documentSides["B1"].grid(column = self.documentSidesGridColumnIndex[5])
                self.documentSides["B2"].grid(column = self.documentSidesGridColumnIndex[3])
                self.documentSides["B3"].grid(column = self.documentSidesGridColumnIndex[1])
            else:
                self.documentSides["B1"].grid(column = self.documentSidesGridColumnIndex[1])
                self.documentSides["B2"].grid(column = self.documentSidesGridColumnIndex[3])
                self.documentSides["B3"].grid(column = self.documentSidesGridColumnIndex[5])
        else: # concatenate
            if self.isReverseDocumentACheckboxValue.get():
                self.documentSides["A1"].grid(column = self.documentSidesGridColumnIndex[2])
                self.documentSides["A2"].grid(column = self.documentSidesGridColumnIndex[1])
                self.documentSides["A3"].grid(column = self.documentSidesGridColumnIndex[0])
            else:
                self.documentSides["A1"].grid(column = self.documentSidesGridColumnIndex[0])
                self.documentSides["A2"].grid(column = self.documentSidesGridColumnIndex[1])
                self.documentSides["A3"].grid(column = self.documentSidesGridColumnIndex[2])
            if self.isReverseDocumentBCheckboxValue.get():
                self.documentSides["B1"].grid(column = self.documentSidesGridColumnIndex[5])
                self.documentSides["B2"].grid(column = self.documentSidesGridColumnIndex[4])
                self.documentSides["B3"].grid(column = self.documentSidesGridColumnIndex[3])
            else:
                self.documentSides["B1"].grid(column = self.documentSidesGridColumnIndex[3])
                self.documentSides["B2"].grid(column = self.documentSidesGridColumnIndex[4])
                self.documentSides["B3"].grid(column = self.documentSidesGridColumnIndex[5])

    def __quit(self):
        self.shelve.close()
        quit()

    def __addSelectDocumentGroups(self):
        docAGroup = LabelFrame(self.rootWindow, text="Document containing odd sheets (A)", padx=5, pady=5)
        docAGroup.pack(padx=10, pady=10, fill='x')
        Button(docAGroup, text="select document", command=self.__onSelectOddPagesCallback).grid(row=0, column=0,
                                                                                                sticky=W)
        self.oddPdfEntry = Entry(docAGroup, width=self.defaultTextfieldWidth)
        self.oddPdfEntry.grid(row=0, column=1, sticky=W)

        isReversedeACheckBtn = Checkbutton(docAGroup, text="read document reversed",
                                           variable=self.isReverseDocumentACheckboxValue,
                                           command=self.__onIsReverseDocumentACheckboxCallback)
        isReversedeACheckBtn.grid(row=1, column=0, sticky=W)
        if self.__isReverseDocumentdA():
            isReversedeACheckBtn.select()

        docBGroup = LabelFrame(self.rootWindow, text="Document containing even sheets (B)", padx=5, pady=5)
        docBGroup.pack(padx=10, pady=10, fill='x')
        Button(docBGroup, text="select document", command=self.__onSelectEvenPagesCallback, justify=LEFT).grid(row=0,
                                                                                                               column=0,
                                                                                                               sticky=W)
        self.evenPdfEntry = Entry(docBGroup, width=self.defaultTextfieldWidth)
        self.evenPdfEntry.grid(row=0, column=1)

        isReversedBCheckBtn = Checkbutton(docBGroup, text="read document reversed",
                                          variable=self.isReverseDocumentBCheckboxValue,
                                          command=self.__onIsReverseDocumentBCheckboxCallback)
        isReversedBCheckBtn.grid(row=1, column=0)
        if self.__isReverseDocumentdB():
            isReversedBCheckBtn.select()

    def __addSelectOutputDocumentGroup(self):
        outDdocGroup = LabelFrame(self.rootWindow, text="Output", padx=5, pady=5)
        outDdocGroup.pack(padx=10, pady=10, fill='x')
        Button(outDdocGroup, text="select otput folder", command=self.__onSelectOutDirectoryCallback).grid(row=0,
                                                                                                           column=0,
                                                                                                           sticky=W)
        self.outPdfEntry = Entry(outDdocGroup, width=self.defaultTextfieldWidth)
        self.outPdfEntry.grid(row=0, column=1)
        self.outPdfEntry.insert(0, self.__lastAccessedFolder() + "/merged.pdf")

    def __addSelectModeGroup(self):
        modeGroup = LabelFrame(self.rootWindow, text="Mode of operation", padx=5, pady=5)
        modeGroup.pack(padx=10, pady=10, fill="x")
        modeRadioBtn = Radiobutton(modeGroup, text="merge page by page", variable=self.operationModeRadioButtonValue,
                                   value="merge",
                                   command=self.__onModeChangedCallback)
        modeRadioBtn.grid(row=0, column=0, sticky=W)
        if self.__operationMode() == "merge":
            modeRadioBtn.select()
        modeRadioBtn = Radiobutton(modeGroup, text="append 2nd document to 1st",
                                   variable=self.operationModeRadioButtonValue, value="concatenate",
                                   command=self.__onModeChangedCallback)
        modeRadioBtn.grid(row=1, column=0, sticky=W)
        if self.__operationMode() == "concatenate":
            modeRadioBtn.select()

    def __addActionGroup(self):

        actionsGroup = LabelFrame(self.rootWindow, text="Merge", padx=5, pady=5)
        actionsGroup.pack(padx=10, pady=10, fill='x')
        actionBtn = Button(actionsGroup, text="merge files", command=self.__mergePdf)
        actionBtn.grid(row=0, column=0, sticky=W)
        doOpenOutput = Checkbutton(actionsGroup, text="open merged result", variable=self.doOpenResultCheckboxValue,
                                   command=self.__onDoOpenResultCheckboxCallback)
        doOpenOutput.grid(row=0, column=1, sticky=W)
        if self.__isOpenResultChecked():
            doOpenOutput.select()

        actionLabel = Label(actionsGroup, text="applied command:")
        actionLabel.grid(row=1, column=0, sticky=W)
        self.actionEntry = Entry(actionsGroup, width=self.defaultTextfieldWidth)
        self.actionEntry.configure(state='readonly')
        self.actionEntry.grid(row=1, column=1)

    def __addIllustrateResultGroup(self):
        group = LabelFrame(self.rootWindow, text="Result illustration")
        group.pack(padx=10, pady=10, fill=X)
        self.garbage = dict()

        Label(group, text="    ").grid(row=0, column=0,sticky=W)
        Label(group, text="input:").grid(row=0, column=1,sticky=W)
        Label(group, text="    ").grid(row=0, column=5,sticky=W)
        Label(group, text="ouput:").grid(row=0, column=6,sticky=W, columnspan=20)

        img = PhotoImage(file=self.shelveDirectory + "/icons/documentA.png")
        Label(group, image=img).grid(row=1, column=1, sticky=W)
        self.garbage[img] = img

        img = PhotoImage(file=self.shelveDirectory + "/icons/documentB.png")
        Label(group, image=img).grid(row=1, column=2, sticky=W)
        self.garbage[img] = img


        self.documentSidesGridColumnIndex = {0:6, 1:7, 2:8, 3:9, 4:10, 5:11}
        self.documentSides = dict()

        img = PhotoImage(file=self.shelveDirectory + "/icons/a1.png")
        l = Label(group, image=img)
        l.grid(row=1, column=6, sticky=W)
        self.documentSides["A1"] = l
        self.garbage[img] = img

        img = PhotoImage(file=self.shelveDirectory + "/icons/a2.png")
        l = Label(group, image=img)
        l.grid(row=1, column=7, sticky=W)
        self.documentSides["A2"] = l
        self.garbage[img] = img

        img = PhotoImage(file=self.shelveDirectory + "/icons/a3.png")
        l = Label(group, image=img)
        l.grid(row=1, column=8, sticky=W)
        self.documentSides["A3"] = l
        self.garbage[img] = img

        img = PhotoImage(file=self.shelveDirectory + "/icons/b1.png")
        l = Label(group, image=img)
        l.grid(row=1, column=9, sticky=W)
        self.documentSides["B1"] = l
        self.garbage[img] = img

        img = PhotoImage(file=self.shelveDirectory + "/icons/b2.png")
        l = Label(group, image=img)
        l.grid(row=1, column=10, sticky=W)
        self.documentSides["B2"] = l
        self.garbage[img] = img

        img = PhotoImage(file=self.shelveDirectory + "/icons/b3.png")
        l = Label(group, image=img)
        l.grid(row=1, column=11, sticky=W)
        self.documentSides["B3"] = l
        self.garbage[img] = img


    def __initWindow(self):
        self.__addSelectDocumentGroups()
        self.__addSelectOutputDocumentGroup()
        self.__addSelectModeGroup()
        self.__addIllustrateResultGroup()
        self.__addActionGroup()
        quitBtn = Button(self.rootWindow, text="quit", command=self.__quit)
        quitBtn.pack()
        self.__addStatusBar()
        self.__updateDocumentIllustration()

    def __mergePdf(self):
        self.__writeToStatusBar("processing ...")
        self.__updateAction()
        if not self.pdftk.invoke() == 0:
            tkMessageBox.showinfo("Error", self.pdftk.getLastMessage())
        else:
            if self.__isOpenResultChecked():
                subprocess.call("xdg-open " + self.pdftk.getOutputDocumentPath(), shell=True)
        self.__writeToStatusBar()

    def __checkForUpdate(self):
        status, isUpdateAvailable = UpdateCheck().checkIfUpdateAvailable()
        if status == 0:
            if isUpdateAvailable:
                self.updateAvailable = True
                self.__writeToStatusBar()

    def __writeToStatusBar(self, text=""):
        format = "%s - %s"
        if text == "" or not self.updateAvailable:
            format = "%s%s"
        updateInfo = ""
        if self.updateAvailable:
            updateInfo = "a newer version is available"
        self.statusBar.config(text=format % (text, updateInfo))
        self.statusBar.update_idletasks()

    def __addStatusBar(self):
        Label(self.rootWindow, pady=2).pack(fill=X)
        self.statusBar = Label(self.rootWindow, text="", bd=1, relief=SUNKEN, anchor=W)
        self.statusBar.pack(side=BOTTOM, fill=X)

    def run(self):
        self.__initWindow()
        self.rootWindow.protocol("WM_DELETE_WINDOW", self.__quit)
        Thread(target=self.__checkForUpdate).start()
        self.rootWindow.mainloop()


if __name__ == '__main__':
    taskPreparationGui = MergePdfGui()
