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

        # Create list of objects representing UI components
        self.object_list = {
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
            "brake": QmlObjectManager(12)
        }

        # Bind created objects to qml context property
        self.rootContext().setContextProperty("rpm_gauge", self.object_list["rpm_gauge"])
        self.rootContext().setContextProperty("gear", self.object_list["gear"])
        self.rootContext().setContextProperty("coolant_tmp", self.object_list["coolant_tmp"])
        self.rootContext().setContextProperty("oil_tmp", self.object_list["oil_tmp"])
        self.rootContext().setContextProperty("oil_pressure", self.object_list["oil_pressure"])
        self.rootContext().setContextProperty("fuel_pressure", self.object_list["fuel_pressure"])
        self.rootContext().setContextProperty("fl_dumper", self.object_list["fl_dumper"])
        self.rootContext().setContextProperty("fr_dumper", self.object_list["fr_dumper"])
        self.rootContext().setContextProperty("rl_dumper", self.object_list["rl_dumper"])
        self.rootContext().setContextProperty("rr_dumper", self.object_list["rr_dumper"])
        self.rootContext().setContextProperty("tps", self.object_list["tps"])
        self.rootContext().setContextProperty("brake", self.object_list["brake"])

        directory = os.path.dirname(os.path.abspath(__file__))
        self.setSource(QUrl.fromLocalFile(os.path.join(directory, "OverviewTab2.qml")))
        self.setResizeMode(QQuickWidget.SizeRootObjectToView)

    def add_config_variable(self, variable):
        self.config_variable_list.append(variable)

    def update_data(self, data_point):
        for obj in self.object_list.values():
            if obj.overview_id == data_point.overview_id:
                obj.value = data_point.value