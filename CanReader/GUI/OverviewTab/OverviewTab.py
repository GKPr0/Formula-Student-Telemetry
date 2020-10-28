from PyQt5 import uic, QtCore
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QAction, QVBoxLayout
from PyQt5.QtCore import QObject, QTimer, QUrl, pyqtSignal, pyqtProperty
import os
from CanReader.GUI.OverviewTab.QmlObjectManager import QmlObjectManager
from CanReader.GUI.Tab import Tab

class OverviewTab(QQuickWidget, Tab):

    update_data_signal = QtCore.pyqtSignal(object)

    def __init__(self):
        QQuickWidget.__init__(self)

        self.group_id = 0
        self.config_variable_list = []
        self.update_data_signal.connect(self.update_data)

        # Create dict of objects representing UI components
        self.object_dict = {
            "rpm_gauge": QmlObjectManager(1),
            "gear": QmlObjectManager(2, type= "int"),
            "coolant_tmp": QmlObjectManager(3),
            "oil_tmp": QmlObjectManager(4),
            "oil_pressure": QmlObjectManager(5),
            "fuel_pressure": QmlObjectManager(6),
            "fl_dumper": QmlObjectManager(7),
            "fr_dumper": QmlObjectManager(8),
            "rl_dumper": QmlObjectManager(9),
            "rr_dumper": QmlObjectManager(10),
            "tps": QmlObjectManager(11),
            "brake": QmlObjectManager(12),
            "battery": QmlObjectManager(13),
            "FPS": QmlObjectManager(14),
            "CFS": QmlObjectManager(15),
            "WBO_sensor": QmlObjectManager(16),
            "FP_sensor" : QmlObjectManager(17),
            "CLT_sensor": QmlObjectManager(18),
            "knock_detect": QmlObjectManager(19)
        }

        for key in self.object_dict:
            self.rootContext().setContextProperty(key, self.object_dict[key])

        directory = os.path.dirname(os.path.abspath(__file__))
        self.setSource(QUrl.fromLocalFile(os.path.join(directory, "OverviewTab2.qml")))
        self.setResizeMode(QQuickWidget.SizeRootObjectToView)

    def add_config_variable(self, variable):
        self.config_variable_list.append(variable)

    def update_data(self, data_point):
        for obj in self.object_dict.values():
            if obj.overview_id == data_point.overview_id:
                obj.value = data_point.value