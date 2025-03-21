from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from app.src.settings_bar import SettingsBar


class MainUI(QWidget):
    def __init__(
        self,
        config=None,
    ):
        super().__init__()
        self.config = config
        
        self.settings_bar = SettingsBar(
            config=self.config,
        )
        
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.settings_bar)
        self.setLayout(main_layout)
    
    
        
        
        
        
        
        
        