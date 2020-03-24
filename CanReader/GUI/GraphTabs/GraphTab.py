from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QAction

class GraphTab(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi('CanReader/GUI/GraphTabs/GraphTab.ui', self)

        self.group_id = 0
