from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame
from datetime import datetime


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
        self.locked = False

        self.update_signal.connect(self.update_data)

        layout = QVBoxLayout()

        img = QPixmap(self.ICONS["Yellow"])
        self.icon = QLabel()
        self.icon.setPixmap(img)
        self.icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon)

        # Name label
        self.name_label = QLabel(self.name)
        self.name_label.setStyleSheet("color: rgb(255,255,255);"
                                      "font: bold \"MS Shell\"; "
                                      "font-size: 9; "
                                      "qproperty-alignment: AlignCenter;")
        self.name_label.setWordWrap(True)
        layout.addWidget(self.name_label)

        # Error layout
        self.error_frame = QFrame()
        error_layout = QHBoxLayout()

        self.time_label = QLabel("")
        self.time_label.setFixedSize(65, 21)
        self.time_label.setStyleSheet("color: rgb(255,0,0);"
                                      "font: \"MS Shell\";"
                                      "font-size: 9;"
                                      "qproperty-alignment: AlignCenter;")
        error_layout.addWidget(self.time_label, alignment=Qt.AlignRight | Qt.AlignHCenter)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setFixedSize(70, 21)
        self.reset_button.setStyleSheet("color: rgb(255,0,0); "
                                        "font: bold \"MS Shell\"; "
                                        "font-size: 9")
        self.reset_button.clicked.connect(self.error_reset)
        error_layout.addWidget(self.reset_button, alignment=Qt.AlignLeft | Qt.AlignHCenter)

        self.error_frame.setLayout(error_layout)
        layout.addWidget(self.error_frame)

        self.setLayout(layout)
        self.error_frame.hide()

    def update_data(self, status):
        """
            :Description:
                Updates status and show appropriate signalization LED.

            :param status: New status value.
            :type status: bool
        """
        if not self.locked and self.status != status:
            self.status = status
            if bool(self.status):
                img = QPixmap(self.ICONS["Red"])
                self.error_received()
            else:
                img = QPixmap(self.ICONS["Green"])

            self.icon.setPixmap(img)

    def error_received(self):
        """
            :Description:
                Used when error status is received.\n
                Shows time of error and reset button.\n
                Locks widget do new states won't change anything.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(timestamp)

        self.name_label.setStyleSheet("color: rgb(255, 0, 0);"
                                      "font: bold \"MS Shell\"; "
                                      "font-size: 9; "
                                      "qproperty-alignment: AlignCenter;")
        self.error_frame.show()
        self.locked = True

    def error_reset(self):
        """
            :Description:
                Event handler for reset button click.\n
                Hide reset button and timestamp.\n
                Sets icon to yellow.\n
                Unlock widget and set state to None.
        """
        img = QPixmap(self.ICONS["Yellow"])
        self.icon.setPixmap(img)

        self.name_label.setStyleSheet("color: rgb(255, 255, 255);"
                                      "font: bold \"MS Shell\"; "
                                      "font-size: 9; "
                                      "qproperty-alignment: AlignCenter;")
        self.error_frame.hide()
        self.locked = False
        self.status = None
