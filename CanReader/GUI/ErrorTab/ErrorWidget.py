from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap

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
        label_img = QLabel()
        label_img.setPixmap(img)
        layout.addWidget(label_img)

        label = QLabel(self.name)
        layout.addWidget(label)

        self.setLayout(layout)

if __name__ == "__main__":
    ICONS = {"Green": 0, "Red": 1, "Yellow": 2}
    print(ICONS["Green"])


