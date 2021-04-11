import datetime

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore
from pyqtgraph import PlotWidget

UNIX_EPOCH = datetime.datetime(1970, 1, 1, 0, 0)  # offset-naive datetime
TS_MULT_us = 1e6


def now_timestamp(ts_mult=TS_MULT_us, epoch=UNIX_EPOCH):
    """
        :Description:
            Used to get current unix timestamp.

        :param ts_mult: Timestamp multiplication.
        :type ts_mult: float

        :param epoch: Unix epoch usually 1.1.1970.
        :type epoch: datetime
    """
    return int((datetime.datetime.utcnow() - epoch).total_seconds()*ts_mult)


def int2dt(ts, ts_mult=TS_MULT_us):
    """
        :Description:
            Used to convert unix timestamp to  UTC datetime.

        :param ts: Unix timestamp ie. number of seconds since 1.1.1970.
        :type ts: int

        :param ts_mult: Timestamp multiplication.
        :type ts_mult: float
    """
    return datetime.datetime.utcfromtimestamp(float(ts)/ts_mult)


class TimeAxisItem(pg.AxisItem):
    """
        :Inherit: :class:`pyqtgraph.AxisItem`

        :Description:
            Used for creating own AxisItem ie. own format of axis.\n
            Own axis shows time in format H:M:S
            For more detail see base class :class:`pyqtgraph.AxisItem`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        return [int2dt(value).strftime("%H:%M:%S") for value in values]

class Graph(PlotWidget):
    """
        :Inherit: :class:`pyqtgraph.PlotWidget`

        :Description:
            Used to create Graph widget.\n
            Controls everything in graph (signals, store values, etc.)

        :param name: Title of the graph.
        :type name: str

        :param unit: Unit which will value on y axis represent.
        :type unit: str

        :param id: Id of widget in group. Used to identify destination of new value.
        :type id: int
    """

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
        """
            :Description:
                Used to change state of the graph.\n
                Based on state of graph refreshes its view or not.

            :param state: New state of the graph.
            :type state: bool
        """
        self.active = state

    def mousePressEvent(self, ev):
        """
            :Description:
                Wrapper on base mousePressEvent.\n
                If left button is pressed activate inspect mode.\n
                In inspect mode user can move, zoom etc. in graph.\n
                Also, graph won't be autofocusing to newest data.

            :param ev: Mouse press event.
            :type ev: GraphicsView.mousePressEvent
        """
        if ev.button() == QtCore.Qt.LeftButton:
            self.inspect_mode = True

        PlotWidget.mousePressEvent(self, ev)

    def mouseReleaseEvent(self, ev):
        """
            :Description:
                Wrapper on base mouseReleaseEvent.\n
                If middle button is released graph will turn on autofocus on newest data and end inspect mode.\n
                If left button is released and view box is on newest data turn on inspect mode will end.

            :param ev: Mouse releae event.
            :type ev: GraphicsView.mouseReleaseEvent
        """
        if ev.button() == QtCore.Qt.MidButton:
            self.auto_focus()
        elif ev.button() == QtCore.Qt.LeftButton:
            if self.is_view_box_on_actual_data():
                self.inspect_mode = False

        PlotWidget.mouseReleaseEvent(self, ev)

    def keyPressEvent(self, ev):
        """
            :Description:
                Wrapper on base keyPressEvent.\n
                If 'c' or 'f' is pressed graph will go to autofocus mode.

            :param ev: Key press event.
            :type ev: GraphicsView.keyPressEvent
        """

        if ev.text() in ['c', 'f']:
            self.auto_focus()
        PlotWidget.keyPressEvent(self, ev)

    def is_view_box_on_actual_data(self):
        """
            :return: True if actual view is on newest data.
            :rtype: bool
        """
        return self.view_back > (now_timestamp() - self.viewRect().x())

    def auto_focus(self):
        """
            :Description:
                Enables auto range mode, which automatically adjust range of Y axis based on shown values.\n
                Turn off inspect mode.
        """
        self.enableAutoRange()
        self.inspect_mode = False

    def setup_graph(self):
        """
            :Description:
                Setup graph background, title, axis. etc.
        """
        self.setBackground((79, 78, 78))
        self.setClipToView(True)
        self.setTitle(self._name, color='#bdbebf', size='10pt', bold=True)
        self.setLabel('left', text=self._unit, color='#bdbebf',  size='15pt')
        self.setLabel('bottom', text='Time', units='', unitPrefix='', color='#bdbebf', size='15pt')
        self.showGrid(x=True, y=True)

    def update_data(self, value):
        """
            :Description:
                Update graph data with new value.\n
                Extend data storage if full.\n
                Redraw graph curve if graph is active.\n
                Adjust X axis range to value array if not in inspect mode.

            :param value: New value to be shown.
            :type value: int, float
        """
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
        """
            :Description:
                Extend data storage arrays by 1000 elements.\n
                Used when the new value does not fit to the array.

        """
        new_size = self.data_x.shape[0] + 1000

        tmp_x = self.data_x
        self.data_x = np.empty(new_size)
        self.data_x[:tmp_x.shape[0]] = tmp_x

        tmp_y = self.data_y
        self.data_y = np.empty(new_size)
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

    graph = Graph("Tests", "Km/hod", 1)

    layout.addWidget(graph)
    window.setLayout(layout)

    tmr = QTimer()
    tmr.timeout.connect(send_data)
    tmr.start(30)
    window.show()

    app.exec_()



