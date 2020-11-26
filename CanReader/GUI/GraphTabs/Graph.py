import numpy as np
import datetime
from PyQt5 import QtCore
from pyqtgraph import PlotWidget
import pyqtgraph as pg

UNIX_EPOCH = datetime.datetime(1970, 1, 1, 0, 0)  # offset-naive datetime
TS_MULT_us = 1e6


def now_timestamp(ts_mult=TS_MULT_us, epoch=UNIX_EPOCH):
    return int((datetime.datetime.utcnow() - epoch).total_seconds()*ts_mult)


def int2dt(ts, ts_mult=TS_MULT_us):
    return datetime.datetime.utcfromtimestamp(float(ts)/ts_mult)


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        return [int2dt(value).strftime("%H:%M:%S") for value in values]

class Graph(PlotWidget):

    update_signal = QtCore.pyqtSignal(float)
    state_signal = QtCore.pyqtSignal(bool)

    def __init__(self, name, unit, id):
        PlotWidget.__init__(self, axisItems={'bottom': TimeAxisItem(orientation='bottom')})

        self._name = name
        self._unit = unit
        self.id = id

        self.update_signal.connect(self.update_data)
        self.state_signal.connect(self.change_state)

        self.setup_graph()

        self.inspect_mode = False
        self.active = False

        self.view_back = 10 * TS_MULT_us
        self.vies_front = 1 * TS_MULT_us

        self.data_x = np.empty(1000)
        self.data_y = np.empty(1000)
        self.ptr = 0

        self.pen = pg.mkPen(color=(255, 255, 255))
        self.curve = self.plot(pen=self.pen)

    def change_state(self, state):
        self.active = state

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            self.inspect_mode = True

        PlotWidget.mousePressEvent(self, ev)

    def mouseReleaseEvent(self, ev):
        if ev.button() == QtCore.Qt.MidButton:
            self.auto_focus()
        elif ev.button() == QtCore.Qt.LeftButton:
            if self.is_view_box_on_actual_data():
                self.inspect_mode = False

        PlotWidget.mouseReleaseEvent(self, ev)

    def keyPressEvent(self, ev):
        print(self.data_x.shape)
        if ev.text() in ['c', 'f']:
            self.auto_focus()
        PlotWidget.keyPressEvent(self, ev)

    def is_view_box_on_actual_data(self):
        return self.view_back > (now_timestamp() - self.viewRect().x())

    def auto_focus(self):
        self.enableAutoRange()
        self.inspect_mode = False

    def setup_graph(self):
        self.setBackground((79, 78, 78))
        self.setClipToView(True)
        self.setTitle(self._name, color='#bdbebf', size='10pt', bold=True)
        self.setLabel('left', text=self._unit, color='#bdbebf',  size='15pt')
        self.setLabel('bottom', text='Time', units='', unitPrefix='', color='#bdbebf', size='15pt')
        self.showGrid(x=True, y=True)

    def update_data(self, value):
        if self.ptr >= self.data_x.shape[0]:
            self.extend_data_storage()

        time_now = now_timestamp()
        self.data_x[self.ptr] = time_now
        self.data_y[self.ptr] = value

        if self.active:
            self.curve.setData(x=self.data_x[:self.ptr], y=self.data_y[:self.ptr])
            if not self.inspect_mode:
                self.setXRange(time_now - self.view_back, time_now + self.vies_front)
        self.ptr += 1

    def extend_data_storage(self):
        tmp_x = self.data_x
        self.data_x = np.empty(self.data_x.shape[0] * 2)
        self.data_x[:tmp_x.shape[0]] = tmp_x

        tmp_y = self.data_y
        self.data_y = np.empty(self.data_y.shape[0] * 2)
        self.data_y[:tmp_y.shape[0]] = tmp_y


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
    from PyQt5.QtCore import QTimer

    value = 1

    def send_data():
        global value
        value += np.random.normal()
        graph.update_signal.emit(value)

    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()

    graph = Graph("Test", "Km/hod", 1)

    layout.addWidget(graph)
    window.setLayout(layout)

    tmr = QTimer()
    tmr.timeout.connect(send_data)
    tmr.start(30)
    window.show()

    app.exec_()



