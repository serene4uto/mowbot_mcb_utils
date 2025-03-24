from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTabWidget,
)
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from app.src.logger import logger
from app.src.settings_bar import SettingsBar
from app.src.serial_service import SerialService
from app.src.monitor_panel import MonitorPanel
from app.src.config_panel import ConfigPanel


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
        self.monitor_panel = MonitorPanel()
        self.config_panel = ConfigPanel()
        self.serial_service = SerialService()     
        
        self.tab_widget = QTabWidget()
        
        self.init_ui()
        
        self.settings_bar.port_connection_request.connect(self.on_port_connection_request)
        # Connect the port_connection_changed signal from the serial service to the settings bar
        self.serial_service.port_connection_changed.connect(self.settings_bar.on_port_connection_changed)
        self.serial_service.rundata_received.connect(self.monitor_panel.on_rundata_received)
        self.config_panel.cfg_update_request.connect(self.on_cfg_return_mode)
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.settings_bar)
        monitor_tab = QWidget()
        monitor_layout = QVBoxLayout()
        monitor_layout.addWidget(self.monitor_panel)
        monitor_tab.setLayout(monitor_layout)
        self.tab_widget.addTab(monitor_tab, "Monitor")
        config_tab = QWidget()
        config_layout = QVBoxLayout()
        config_layout.addWidget(self.config_panel)
        config_tab.setLayout(config_layout)
        self.tab_widget.addTab(config_tab, "Config")
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)
        
    @pyqtSlot(str)
    def on_port_connection_request(self, port_name):
        if port_name == "Close":
            if self.serial_service.running_:
                self.serial_service.stop()
        else:
            if self.serial_service.running_:
                self.serial_service.stop()
            self.serial_service.start(port_name)
    
    @pyqtSlot(str)
    def on_cfg_return_mode(self, mode):
        # logger.info(f"Setting return mode to {mode}")
        self.serial_service.cfg_return_mode(mode)
        
        
    
    
        
        
        
        
        
        
        