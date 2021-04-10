from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


class QmlObjectManager(QObject):
    """
        :Inherit: :class:`QObject`

        :Description:
            Class used to create communication bridge between python variables and qml variables.

        :param overview_id: Id of variable in overview.
        :type overview_id: int

        :param type: Type of input variable int.
        :type type: str

        :param parent: Parent of the object.
        :type parent: QObject
    """
    value_changed_signal = pyqtSignal()

    def __init__(self, overview_id, type="str", parent=None):
        QObject.__init__(self, parent)
        self._value = "0"
        self.type = type
        self.overview_id = overview_id

    @pyqtProperty(str, notify=value_changed_signal)
    def value(self):
        """
            :Description:
                Getter for object value.

            :return: Value.
            :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
            :Description:
                Setter for object value.

            :param value: Value to be set.
            :type value: str, int, float
        """
        if self.type == "int":
            value = round(value)

        value = str(value)
        if self._value == value:
            return
        self._value = value
        self.value_changed_signal.emit()
