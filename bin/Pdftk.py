
import subprocess
import commands

class Pdftk:
    def __init__(self):
        self.binary = "pdftk"
        self.documentOrder = {"normal": "1-end", "reversed": "end-1"}
        self.operationModes = {"merge": "shuffle", "concatenate": "cat"}
        self.update()

    def getOutputDocumentPath(self):
        return self.outputDocument

    def invoke(self):
        status, output = commands.getstatusoutput(self.getCommandString())
        if status == 0:
            self.lastMessage = ""
        else:
            self.lastMessage = output
        return status

    def getLastMessage(self):
        return self.lastMessage

    def update(self, documentA="", documentB = "", outputDocument = "merge.pdf",
               documentAOrder="normal", documentBOrder="reversed", operationMode="merge"):
        self.documentA = documentA
        self.documentB = documentB
        self.outputDocument = outputDocument
        self.documentAOrder = self.documentOrder[documentAOrder]
        self.documentBOrder = self.documentOrder[documentBOrder]
        self.operationMode = self.operationModes[operationMode]


    def getCommandString(self):
        return "%s A=%s B=%s %s A%s B%s output %s" % (
            self.binary,
            self.documentA,
            self.documentB,
            self.operationMode,
            self.documentAOrder,
            self.documentBOrder,
            self.outputDocument)
