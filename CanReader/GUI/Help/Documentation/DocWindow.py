from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os
import sys


class DocWindow(QMainWindow):
    """
        :Inherit: :class:`QMainWindow`

        :Description:
            Open documentation in Qt WebEngine
    """
    def __init__(self, *args, **kwargs):
        super(QMainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Documentation")
        self.setWindowIcon(QIcon(os.path.join(sys.path[0], "Images/question_black.svg")))

        doc_path = os.path.abspath(os.path.join(sys.path[0], "../Docs/build/html/index.html"))

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl.fromLocalFile(doc_path))
        self.setCentralWidget(self.browser)

        self.show()
