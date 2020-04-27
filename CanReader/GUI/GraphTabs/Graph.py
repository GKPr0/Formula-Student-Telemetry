from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QAction
from PyQt5.QtGui import QColor
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from random import randint


class Graph(PlotWidget):

    update_signal = QtCore.pyqtSignal(float)

    def __init__(self, name, unit, id):
        PlotWidget.__init__(self)

        self._name = name
        self._unit = unit
        self.id = id

        self.update_signal.connect(self.update_data)
        self.setup_graph()

        #Setup data
        self.x = list(range(3))
        self.y = [0,0,0]
        self.pen = pg.mkPen(color=(255, 255, 255))
        self.data_line = self.plot(self.x, self.y, pen=self.pen)


    def setup_graph(self):
        self.setBackground((79, 78, 78))
        self.setTitle(self._name, color='#bdbebf', size='10pt',bold = True)
        self.setLabel('left', self._unit, color='#bdbebf',  size='15pt')
        self.setLabel('bottom', 'Sample', color='#bdbebf', size='15pt')
        self.showGrid(x=True, y=True)

    def update_data(self, value):
        self.x = self.x[1:]
        self.x.append(self.x[-1] + 1)

        self.y = self.y[1:]
        self.y.append(value)

        self.data_line.setData(self.x, self.y)  # Update the data.
