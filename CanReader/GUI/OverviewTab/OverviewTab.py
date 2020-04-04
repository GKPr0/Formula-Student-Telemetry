from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QAction
from CanReader.GUI.Tab import Tab

class OverviewTab(Tab):

    def __init__(self):
        Tab.__init__(self)
        uic.loadUi('CanReader/GUI/OverviewTab/OverViewTab.ui', self)






