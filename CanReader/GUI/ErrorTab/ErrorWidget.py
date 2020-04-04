from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QFont

from CanReader.GUI.GraphTabs.Graph import Graph


class ErrorWidget(QWidget):

    ICONS = {
        "Green": "CanReader/Images/green_led.png",
        "Red": "CanReader/Images/red_led.png",
        "Yellow": "CanReader/Images/yellow_led.png"
    }

    def __init__(self, name):
        QWidget.__init__(self)

        self.name = name
        self.status = None

        layout = QVBoxLayout()

        img = QPixmap(self.ICONS["Yellow"])
        self.label_img = QLabel()
        self.label_img.setPixmap(img)
        self.label_img.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_img)

        label = QLabel(self.name)
        font = QFont("MS Shell", 9, QFont.Bold)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.setLayout(layout)

    def update_status(self, status):
        self.status = status

        if self.status:
            img = QPixmap(self.ICONS["Red"])
        else:
            img = QPixmap(self.ICONS["Green"])

        self.label_img.setPixmap(img)
