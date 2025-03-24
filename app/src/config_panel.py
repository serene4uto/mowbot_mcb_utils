from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
)
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from app.src.logger import logger 

from app.src import mcb_regs
from app.src.mcb import MCBDataReturnMode

class ConfigItem(QWidget):
    def __init__(self, name):
        super().__init__()
        
        self.name_lbl = QLabel(name + ":")
        self.name_lbl.setFixedWidth(70)
        self.value_lbl = QLabel("N/A")
        self.value_lbl.setFixedWidth(50)
        self.value_le = QLineEdit("")
        self.value_le.setFixedWidth(50)
        self.cfg_btn = QPushButton("Cfg")
        self.cfg_btn.setFixedWidth(50)   
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout()
        layout.addWidget(self.name_lbl)
        layout.addSpacing(0)
        layout.addWidget(self.value_lbl)
        layout.addWidget(self.value_le)
        layout.addWidget(self.cfg_btn)
        layout.addStretch(1)
        self.setLayout(layout)
    
    def update_value_lbl(self, val):
        self.value_lbl.setText(str(val))
        
    def get_value(self):
        return self.value_le.text()
        
    def set_cfg_btn_callback(self, callback):
        self.cfg_btn.clicked.connect(callback)
        
        
class GeneralConfig(QWidget):
    def __init__(
        self
    ):
        super().__init__()
        
        self.gb = QGroupBox("General Config")
        self.gb_layout = QVBoxLayout()
        self.cfg_pwm_type = ConfigItem("PWM Type")
        
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        self.gb_layout.addWidget(self.cfg_pwm_type)
        self.gb.setLayout(self.gb_layout)
        main_layout.addWidget(self.gb)
        main_layout.addStretch(1)
        self.setLayout(main_layout)
        

class MotorConfig(QWidget):
    def __init__(
        self,
        motor_id
    ):
        super().__init__()
        
        self.gb = QGroupBox("Motor " + str(motor_id))
        self.gb_layout = QVBoxLayout()
        
        self.cfg_motor_mode = ConfigItem("Mode")
        
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        self.gb_layout.addWidget(self.cfg_motor_mode)
        self.gb.setLayout(self.gb_layout)
        main_layout.addWidget(self.gb)
        main_layout.addStretch(1)
        self.setLayout(main_layout)
    

class ConfigPanel(QWidget):
    
    cfg_request = pyqtSignal(dict)
    cfg_update_request = pyqtSignal(str)
    
    def __init__(
        self
    ):
        super().__init__()
        
        self.gb = QGroupBox("Config Panel")
        self.gb_layout = QVBoxLayout()
        
        self.general_config = GeneralConfig()
        self.m1_config = MotorConfig(1)
        self.m2_config = MotorConfig(2)
        self.cfg_update_btn = QPushButton("Update Cfg")
        self.init_ui()
        self.init_cfg_btn()
        self.cfg_update_btn.clicked.connect(self.on_cfg_update_btn)
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        self.gb_layout.addWidget(self.general_config)
        motor_layout = QHBoxLayout()
        motor_layout.addWidget(self.m1_config)
        motor_layout.addWidget(self.m2_config)
        self.gb_layout.addLayout(motor_layout)
        self.gb_layout.addStretch(1)
        self.gb.setLayout(self.gb_layout)
        main_layout.addWidget(self.gb)
        utils_layout = QHBoxLayout()
        utils_layout.addWidget(self.cfg_update_btn)
        utils_layout.addStretch(1)
        main_layout.addLayout(utils_layout)
        main_layout.addStretch(1)
        self.setLayout(main_layout)
        
    @pyqtSlot(dict)
    def on_setdata_received(self, data):
        self.general_config.cfg_pwm_type.update_value_lbl(data["pwmportconfig"])
        self.m1_config.cfg_motor_mode.update_value_lbl(data["m1mode"])
        self.m2_config.cfg_motor_mode.update_value_lbl(data["m2mode"])
    
    def on_cfg_update_btn(self):
        self.cfg_update_request.emit("SET")
        
    def init_cfg_btn(self):
        # general
        self.general_config.cfg_pwm_type.set_cfg_btn_callback(
            lambda: self.cfg_request.emit(
                {
                    "reg": mcb_regs.MCB_PWM_PORT_CONFIG_REG,
                    "val": int(self.general_config.cfg_pwm_type.get_value())
                }
            )
        )
        # m1 motor
        self.m1_config.cfg_motor_mode.set_cfg_btn_callback(
            lambda: self.cfg_request.emit(
                {
                    "reg": mcb_regs.MCB_MOTOR1_MODE_REG,
                    "val": int(self.m1_config.cfg_motor_mode.get_value())
                }
            )
        )
        # m2 motor
        self.m2_config.cfg_motor_mode.set_cfg_btn_callback(
            lambda: self.cfg_request.emit(
                {
                    "reg": mcb_regs.MCB_MOTOR2_MODE_REG,
                    "val": int(self.m2_config.cfg_motor_mode.get_value())
                }
            )
        )
        