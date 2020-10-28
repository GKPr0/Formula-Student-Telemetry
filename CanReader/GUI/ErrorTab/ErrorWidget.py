from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5 import QtCore

from GUI.GraphTabs.Graph import Graph


class ErrorWidget(QWidget):

    ICONS = {
        "Green": "CanReader/Images/green_led.png",
        "Red": "CanReader/Images/red_led.png",
        "Yellow": "CanReader/Images/yellow_led.png"
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
        if self.status != status:
            self.status = status
            if bool(self.status):
                img = QPixmap(self.ICONS["Red"])
            else:
                img = QPixmap(self.ICONS["Green"])

            self.label_img.setPixmap(img)
