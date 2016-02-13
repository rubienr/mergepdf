#
# @author rubienr 2/2016
#
from os import path
from os import chdir
import subprocess

class UpdateCheck:
    def __init__(self):
        abspath = path.abspath(__file__)
        self.basedir = path.dirname(abspath)

    def checkIfUpdateAvailable(self):
        chdir(self.basedir)

        try:
            subprocess.check_output(["git","remote update"], shell=True) # timeout=10
            output = subprocess.check_output(["git", "status -uno"], shell=True) # timeout=1
            if "branch is up-to-date" in output:
                return (0, False)
            else:
                return (0, True)
        except subprocess.CalledProcessError as e:
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
