from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


class QmlObjectManager(QObject):
    value_changed_signal = pyqtSignal()

    def __init__(self, overview_id, type="str", parent=None):
        QObject.__init__(self, parent)
        self._value = "0"
        self.type = type
        self.overview_id = overview_id

    @pyqtProperty(str, notify=value_changed_signal)
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self.type == "int":
            value = round(value)

        value = str(value)
        if self._value == value:
            return
        self._value = value
        self.value_changed_signal.emit()
