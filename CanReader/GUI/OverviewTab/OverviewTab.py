from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QAction

class OverviewTab(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi('CanReader/GUI/OverviewTab/OverViewTab.ui', self)

        self.group_id = 1

