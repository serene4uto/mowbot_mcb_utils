from PyQt5.QtWidgets import QMainWindow
from app_info import __app_name__


class MainWindow(QMainWindow):
    def __init__(
        self,
        app,
        config,
    ):
        super().__init__()
        self.setWindowTitle(__app_name__)