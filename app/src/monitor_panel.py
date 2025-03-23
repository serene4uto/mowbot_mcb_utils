from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
)

from PyQt5.QtCore import pyqtSignal, pyqtSlot

class InfoItem(QWidget):
    def __init__(self, name):
        super().__init__()
        
        self.name_lbl = QLabel(name + ":")
        self.name_lbl.setFixedWidth(100)
        self.value_lbl = QLabel("N/A")
        self.value_lbl.setFixedWidth(50)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout()
        layout.addWidget(self.name_lbl)
        layout.addSpacing(0)
        layout.addWidget(self.value_lbl)
        self.setLayout(layout)
        
    def update_value(self, val):
        self.value_lbl.setText(str(val))

class GeneralPanel(QWidget):
    def __init__(self):
        super().__init__()
        
        self.main_layout = QVBoxLayout()
        self.gb = QGroupBox("General Panel")
        self.gb_layout = QHBoxLayout()
        
        self.supply_vol_info = InfoItem("Supply Voltage (V)")
        
        self.init_ui()
    
    def init_ui(self):
        self.gb_layout.addWidget(self.supply_vol_info)
        self.gb_layout.addSpacing(20)
        self.gb_layout.addStretch(1) # Add stretch to push the supply voltage info to the left
        self.gb.setLayout(self.gb_layout)
        self.main_layout.addWidget(self.gb)
        self.setLayout(self.main_layout)
    
    def update_supply_voltage(self, voltage):
        self.supply_vol_info.update_value(voltage)


class MotorStatusItem(QWidget):
    def __init__(self, name, n_motors):
        super().__init__()
        
        self.name_lbl = QLabel(name + ":")
        self.name_lbl.setFixedWidth(150)
        self.n_motors = n_motors
        self.status_lbls = []
        for i in range(n_motors):
            lbl = QLabel("N/A")
            lbl.setFixedWidth(50)
            self.status_lbls.append(lbl)    
        
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        status_layout = QHBoxLayout()
        status_layout.addWidget(self.name_lbl)
        for lbl in self.status_lbls:
            status_layout.addWidget(lbl)
        layout.addLayout(status_layout)
        self.setLayout(layout)

    def update_status(self, status):
        for i, lbl in enumerate(self.status_lbls):
            if status[i] == 0:
                lbl.setText("Normal")
                lbl.setStyleSheet("color: green")
            else:
                lbl.setText("Error")
                lbl.setStyleSheet("color: red")


class MotorPanel(QWidget):
    def __init__(self, motor_id):
        super().__init__()
        
        self.gb = QGroupBox(f"Motor {motor_id}")
        self.gb_layout = QHBoxLayout()
        
        self.speed_info = InfoItem("Speed (RPM)")
        self.current_info = InfoItem("Current (mA)")
        self.temp_info = InfoItem("Temp (*C)")
        
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        m_info_layout = QVBoxLayout()
        main_layout.addWidget(self.gb)
        m_info_layout.addWidget(self.speed_info)
        m_info_layout.addWidget(self.current_info)
        m_info_layout.addWidget(self.temp_info)
        m_info_layout.addStretch(1)
        self.gb_layout.addLayout(m_info_layout)
        self.gb.setLayout(self.gb_layout)
        self.setLayout(main_layout)
    
    def update_motor_speed(self, speed):
        self.speed_info.update_value(speed)
        
    def update_motor_current(self, current):    
        self.current_info.update_value(current)
        
    def update_motor_temperature(self, temp):
        self.temp_info.update_value(temp)


class MotorStatusPanel(QWidget):
    def __init__(self):
        super().__init__()
        
        self.gb = QGroupBox("Motor Status")
        self.gb_layout = QVBoxLayout()
        
        self.stt_current_overload = MotorStatusItem("Current Overload", 2)
        self.stt_load_abnormal = MotorStatusItem("Load Abnormal", 2)
        self.stt_temp_protection = MotorStatusItem("Temperature Protection", 2)
        self.stt_voltage_too_high = MotorStatusItem("Voltage Too High", 2)
        self.stt_voltage_too_low = MotorStatusItem("Voltage Too Low", 2)
        self.stt_blocking_protection = MotorStatusItem("Blocking Protection", 2)
        self.stt_hall_signal_abnormal = MotorStatusItem("Hall Signal Abnormal", 2)
        self.stt_abnormal = MotorStatusItem("Abnormal", 2)
        
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        self.gb_layout.addWidget(self.stt_current_overload)
        self.gb_layout.addWidget(self.stt_load_abnormal)
        self.gb_layout.addWidget(self.stt_temp_protection)
        self.gb_layout.addWidget(self.stt_voltage_too_high)
        self.gb_layout.addWidget(self.stt_voltage_too_low)
        self.gb_layout.addWidget(self.stt_blocking_protection)
        self.gb_layout.addWidget(self.stt_hall_signal_abnormal)
        self.gb_layout.addWidget(self.stt_abnormal)
        self.gb.setLayout(self.gb_layout)
        main_layout.addWidget(self.gb)
        self.setLayout(main_layout)


class MonitorPanel(QWidget):
    
    
    def __init__(self):
        super().__init__()
        
        self.gb = QGroupBox("Monitor Panel")
        self.gb_layout = QVBoxLayout()
        
        self.general_panel = GeneralPanel()
        self.m1_panel = MotorPanel(1)
        self.m2_panel = MotorPanel(2)
        self.motor_status_panel = MotorStatusPanel()
        
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        self.gb_layout.addWidget(self.general_panel)
        motor_layout = QHBoxLayout()
        motor_layout.addWidget(self.m1_panel)
        motor_layout.addWidget(self.m2_panel)
        motor_layout.addWidget(self.motor_status_panel)
        self.gb_layout.addLayout(motor_layout)
        self.gb_layout.addStretch(1)
        self.gb.setLayout(self.gb_layout)
        main_layout.addWidget(self.gb)
        main_layout.addStretch(1)
        self.setLayout(main_layout)
        

    @pyqtSlot(dict)
    def on_rundata_received(self, data):
        self.general_panel.update_supply_voltage(data["supply_vol"])
        self.m1_panel.update_motor_speed(data["m1rpm"])
        self.m1_panel.update_motor_current(data["m1current"])
        self.m1_panel.update_motor_temperature(data["m1temp"])
        self.m2_panel.update_motor_speed(data["m2rpm"])
        self.m2_panel.update_motor_current(data["m2current"])
        self.m2_panel.update_motor_temperature(data["m2temp"])
        
        self.motor_status_panel.stt_current_overload.update_status(
            [data["m1status"]["current_overload"], data["m2status"]["current_overload"]]
        )
        self.motor_status_panel.stt_load_abnormal.update_status(
            [data["m1status"]["load_abnormal"], data["m2status"]["load_abnormal"]]
        )
        self.motor_status_panel.stt_temp_protection.update_status(
            [data["m1status"]["temperature_protection"], data["m2status"]["temperature_protection"]]
        )
        self.motor_status_panel.stt_voltage_too_high.update_status(
            [data["m1status"]["voltage_too_high"], data["m2status"]["voltage_too_high"]]
        )
        self.motor_status_panel.stt_voltage_too_low.update_status(
            [data["m1status"]["voltage_too_low"], data["m2status"]["voltage_too_low"]]
        )
        self.motor_status_panel.stt_blocking_protection.update_status(
            [data["m1status"]["blocking_protection"], data["m2status"]["blocking_protection"]]
        )
        self.motor_status_panel.stt_hall_signal_abnormal.update_status(
            [data["m1status"]["hall_signal_abnormal"], data["m2status"]["hall_signal_abnormal"]]
        )
        self.motor_status_panel.stt_abnormal.update_status(
            [data["m1status"]["abnormal"], data["m2status"]["abnormal"]]
        )