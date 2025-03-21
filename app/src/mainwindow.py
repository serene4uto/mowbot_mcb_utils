from PyQt5.QtWidgets import (
    QMainWindow,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)
from app.app_info import __appname__, __appdescription__

from app.src.mainUI import MainUI


class MainWindow(QMainWindow):
    def __init__(
        self,
        app = None,
        config = None,
    ):
        super().__init__()
        
        self.app = app
        self.config = config
        
        
        # Set the window title
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle(__appname__)
        
        # Set the central widget and the main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        ui_widget = MainUI(
            config=self.config,
        )
        main_layout.addWidget(ui_widget)    
        
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        
        status_bar = QStatusBar()
        status_bar.showMessage(f"{__appname__} - {__appdescription__}")
        self.setStatusBar(status_bar)