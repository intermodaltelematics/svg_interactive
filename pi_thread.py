from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtXml import *
from PyQt5.QtSvg import *

from pi_api import change_state


class PiThread(QThread):
    read_result = pyqtSignal("PyQt_PyObject")
    change_result = pyqtSignal("PyQt_PyObject")

    def __init__(self, address, state_to_change, state_to_read, parent=None):
        super(PiThread, self).__init__(parent)
        self.address = address
        self.state_to_change = state_to_change
        self.state_to_read = state_to_read

    def run(self):
        print("inside Thread..")

        if self.state_to_change:
            from time import sleep

            for _ in range(10):
                self.read_result.emit((self.address, self.state_to_change))
                sleep(1)

        if self.state_to_read:
            self.change_result.emit("Hello changed something")


class SomeThread(QThread):
    pass


def read_something():
    """ logic to read data from the pi 
        needs address
    """
    data = [1, 2, 3, 4]

    # 1. get some data
    for x in data:
        continue

    # 2. parse data
    # 3. check somewthging
    # 4. error handle something
    # 5. return data
    pass
