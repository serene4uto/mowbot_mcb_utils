
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QMessageBox,
    QLabel,
)
from PyQt5.QtCore import pyqtSignal, pyqtSlot

import serial.tools.list_ports


class SerialComboBox(QComboBox):
    
    CURRENT_SERIAL_PORTS = {}
    
    def __init__(
        self
    ):
        super().__init__()
        
    def showPopup(self):
        self.load_available_ports()
        super().showPopup()
    
    def load_available_ports(self):
        try:
            # only get port with name includes "USB" (Linux) or "COM" (Windows)
            port_lists = [
                port for port in serial.tools.list_ports.comports() if "USB" in port.device or "COM" in port.device
            ]
            if port_lists:
                self.clear()
                self.CURRENT_SERIAL_PORTS = {}
                for port in port_lists:
                    self.CURRENT_SERIAL_PORTS[port.device] = port.device
                    self.addItem(port.device)
            else:
                self.clear()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Fails to get serial ports: {str(e)}",
            )
            self.clear()
            
            
class SettingsBar(QtWidgets.QWidget):
    
    port_connection_request = pyqtSignal(str)
    
    def __init__(
        self, 
        config=None
    ):
        super().__init__()
        self.config = config
        
        self.port_connected = False
        
        main_layout = QVBoxLayout()
        group_box = QGroupBox("Settings")
        
        
        self.port_select_cb = SerialComboBox()
        port_select_lbl = QLabel("Port:")
        group_box_layout = QHBoxLayout()
        self.port_connection_btn = QtWidgets.QPushButton("Open")
        
        group_box_layout.addWidget(port_select_lbl)
        port_select_lbl.setFixedWidth(30)
        group_box_layout.addWidget(self.port_select_cb)
        group_box_layout.addSpacing(0)
        self.port_select_cb.setEnabled(True)
        self.port_select_cb.setFixedWidth(100)
        self.port_connection_btn.setFixedWidth(50)
        group_box_layout.addWidget(self.port_connection_btn)
        group_box_layout.addStretch(1)
        group_box.setLayout(group_box_layout)
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)
        
        self.port_connection_btn.clicked.connect(self.on_port_connection_btn)
        
    def on_port_connection_btn(self):
        if self.port_connected:
            self.port_connection_btn.setText("Closing...")
            self.port_connection_btn.setEnabled(False)
            self.port_connection_request.emit("Close")
        else:
            port_name = self.port_select_cb.currentText()
            if port_name is not None:
                self.port_select_cb.setEnabled(False)
                self.port_connection_btn.setText("Opening...")
                self.port_connection_btn.setEnabled(False)
                self.port_connection_request.emit(port_name)
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "No port selected",
                )
                
    
    @pyqtSlot(bool)
    def on_port_connection_changed(self, connected):
        self.port_connected = connected
        if self.port_connected:
            self.port_connection_btn.setText("Close")
            self.port_connection_btn.setEnabled(True)
            self.port_connected = True
        else:
            self.port_connection_btn.setText("Open")
            self.port_connection_btn.setEnabled(True)
            self.port_connected = False
            self.port_select_cb.setEnabled(True)
            
    

            
        
        
        