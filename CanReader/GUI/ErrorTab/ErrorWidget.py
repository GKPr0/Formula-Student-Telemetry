from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class ErrorWidget(QWidget):
    """
        :Inherit: :class:`QWidget`

        :Description:
            Error widget is used to indicate state of binary variable.\n
            States are as follow:
            1. OK -> Green LED
            2. No data -> Yellow LED
            3. Error -> Red Led

        :param name: The name of the variable it signals.
        :type name: str

        :param id: CAN ID used to identify where data should be send.
        :param id: str

        .. note::
            In future this should be implemented:
                1. System to recognize OK from No data ie. Error should be as 0 and OK as 1.
                2. Do not change state once was changed to ERROR until user manually resets.
                3. On Error show label with timestamp showing time of ERROR.
    """

    ICONS = {
        "Green": "Images/green_led.png",
        "Red": "Images/red_led.png",
        "Yellow": "Images/yellow_led.png"
    }

    update_signal = QtCore.pyqtSignal(float)

    def __init__(self, name, id):
        QWidget.__init__(self)

        self.name = name
        self.id = id
        self.status = None

        self.update_signal.connect(self.update_data)

        layout = QVBoxLayout()

        img = QPixmap(self.ICONS["Yellow"])
        self.label_img = QLabel()
        self.label_img.setStyleSheet("border: 0px")
        self.label_img.setPixmap(img)
        self.label_img.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_img)

        label = QLabel(self.name)
        label.setStyleSheet("border: 0px")
        font = QFont("MS Shell", 9, QFont.Bold)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        layout.addWidget(label)

        self.setLayout(layout)

    def update_data(self, status):
        """
            :Description:
                Updates status and show appropriate signalization LED.

            :param status: New status value.
            :type status: bool
        """
        if self.status != status:
            self.status = status
            if bool(self.status):
                img = QPixmap(self.ICONS["Red"])
            else:
                img = QPixmap(self.ICONS["Green"])

            self.label_img.setPixmap(img)
