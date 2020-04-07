from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QAction
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from random import randint


class Graph(PlotWidget):

    def __init__(self, name, unit, id):
        PlotWidget.__init__(self)

        self._name = name
        self._unit = unit
        self.id = id

        self.setup_graph()

        #Setup data
        self.x = list(range(3))
        self.y = [0,0,0]
        self.pen = pg.mkPen(color=(0, 0, 0))
        self.data_line = self.plot(self.x, self.y, pen=self.pen)


    def setup_graph(self):
        self.setBackground("w")
        self.setTitle(self._name, color=(0, 0, 0), size='10pt',bold = True)
        self.setLabel('left', self._unit, color='black', size='15pt')
        self.setLabel('bottom', 'Hour [Hod]', color='black', size='15pt')
        self.showGrid(x=True, y=True)

    def update_data(self, value):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append(value)  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.
