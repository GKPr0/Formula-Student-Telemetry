from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from CanReader.GUI.GraphTabs.Graph import Graph
from CanReader.GUI.Tab import Tab

class ErrorTab(Tab):

    def __init__(self, group_id):
        Tab.__init__(self, group_id)
