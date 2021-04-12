from PyQt5 import uic
from PyQt5.QtGui import QDialog


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        uic.loadUi('GUI/Help/AboutWindow/AboutDialog.ui', self)
        self.show()
