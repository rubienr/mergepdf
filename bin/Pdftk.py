#
# @author rubienr 2/2016
#
import subprocess

class Pdftk:
    def __init__(self):
        self.binary = "pdftk"
        self.documentOrder = {"normal": "1-end", "reversed": "end-1"}
        self.operationModes = {"merge": "shuffle", "concatenate": "cat"}
        self.update()

    def getOutputDocumentPath(self):
        return self.outputDocument

    def invoke(self):
        try:
            output = subprocess.check_output([self.binary + " " + self.__getCommandArguments()], shell=True)
            self.lastMessage = ""
            return 0
        except subprocess.CalledProcessError as e:
            self.lastMessage = e.output
            print("error: " + e.output)
            return 1

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

    def __getCommandArguments(self):
        return "A=%s B=%s %s A%s B%s output %s" % (
            self.documentA,
            self.documentB,
            self.operationMode,
            self.documentAOrder,
            self.documentBOrder,
            self.outputDocument)

    def getCommandString(self):
        return self.binary + " " + self.__getCommandArguments()
