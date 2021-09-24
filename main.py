from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from subprocess import call

class ui_Dialog(QMainWindow):
    def __init__(self):
        super(ui_Dialog, self).__init__()
        loadUi("mainwindow.ui", self)
        self.start.clicked.connect(self.runstr)
        self.instruction.clicked.connect(self.runins)
        self.about.clicked.connect(self.runabt)
        self._new_window = None
    @pyqtSlot()
    def menu(self):
        self._new_window.hide()
        self._new_window = ui_Dialog()
        self._new_window.show()
    def runins(self):
        """
        Called when the user presses the Run button
        """
        ui.hide()
        self.instructionfunc()

    def runabt(self):
        """
        Called when the user presses the Run button
        """
        ui.hide()
        self.aboutfunc()
    def runstr(self):
        """
        Called when the user presses the Run button
        """
        ui.hide()  # hide the main window
        self.startfunc()  # Create and open new output window
    def instructionfunc(self):
        self._new_window = loadUi("instruction.ui", self)
        self._new_window.show()
        self.next1.clicked.connect(self.instruction1)
        self.menuinstruction.clicked.connect(self.menu)

    def instruction1(self):
        self._new_window = loadUi("instruction1.ui", self)
        self._new_window.show()
        self.next2.clicked.connect(self.instruction2)
        self.menuinstruction1.clicked.connect(self.menu)
        self.previous1.clicked.connect(self.instructionfunc)

    def instruction2(self):
        self._new_window = loadUi("instruction2.ui", self)
        self._new_window.show()
        self.next3.clicked.connect(self.instruction3)
        self.menuinstruction2.clicked.connect(self.menu)
        self.previous2.clicked.connect(self.instruction1)

    def instruction3(self):
        self._new_window = loadUi("instruction3.ui", self)
        self._new_window.show()
        self.menuinstruction3.clicked.connect(self.menu)
        self.previous3.clicked.connect(self.instruction2)

    def aboutfunc(self):
        self._new_window = loadUi("about.ui", self)
        self._new_window.show()
        self.menuabout.clicked.connect(self.menu)

    def startfunc(self):
        call(["python", "test.py"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = ui_Dialog()
    ui.show()
    widget = QtWidgets.QStackedWidget
    sys.exit(app.exec_())