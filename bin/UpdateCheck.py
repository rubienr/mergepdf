from os import path
from os import chdir
import commands

class UpdateCheck:
    def __init__(self):
        abspath = path.abspath(__file__)
        self.basedir = path.dirname(abspath)

    def checkIfUpdateAvailable(self):
        chdir(self.basedir)
        status, output = commands.getstatusoutput("git remote update")
        if status == 0:
            status, output = commands.getstatusoutput("git status -uno")
            if status == 0:
                if "branch is up-to-date" in output:
                    return (0, False)
                else:
                    return (0, True)
        return (1, False)

if __name__ == "__main__":
    uc = UpdateCheck()
    status, isUpdateAvailable = uc.checkIfUpdateAvailable()
    if status == 0:
        if isUpdateAvailable:
            print("update available")
        else:
            print("already up to date")
    else:
        print("what a terrible failure")