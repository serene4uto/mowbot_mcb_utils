
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
import serial
from ctypes import c_ubyte
import threading

from app.src.logger import logger

from app.src import mcb_regs
from app.src.mcb import (
    MCBDataReturnMode,
    mcb_run_data_parser,
    mcb_set_data_parser, MCB_MSG_H1, MCB_MSG_H2, MCB_MSG_TX_CMD, MCB_MSG_RX_CMD,
    MBBMC_MSG_SET_DATA_LEN
)


        
class SerialService(QObject):
    
    port_connection_changed = pyqtSignal(bool)
    rundata_received = pyqtSignal(dict)
    setdata_received = pyqtSignal(dict)
    
    serial_lock = threading.Lock()
    
    def __init__(
        self
    ):
        super().__init__()
        
        self.serial_port = None
        self.baudrate = 19200
        self.running_ = False
        
        self.serial = serial.Serial()
        
        self.thread = QThread()
        self.moveToThread(self.thread)
        
        self.thread.started.connect(self._serial_handle_thread)
        
        self.mcb_return_mode = MCBDataReturnMode.RUN
        
        
        
    def _serial_handle_thread(self):
        
        try:
            self.serial = serial.Serial(
                port=self.serial_port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            if self.serial.is_open:
                self.port_connection_changed.emit(True)
                self.running_ = True
                logger.info(f"Opened port {self.serial_port}")
                buffer = bytearray()  # Buffer to accumulate data
                frame_start_sequence = bytearray([0x5A, 0xA5])  # Define the start sequence
                frame_active = False  # Flag to indicate if we're within a frame
                self.cfg_return_mode("RUN")
                while self.running_:
                    
                    # Read one byte at a time
                    data = self.serial.read(1)
                    if data:
                        # Add the byte to the buffer
                        buffer.extend(data)

                        # Check if the buffer has detected the start sequence
                        if len(buffer) >= 2 and buffer[-2:] == frame_start_sequence:
                            if frame_active:
                                # If a frame was active, we have reached the start of the next frame
                                # Print the previous frame
                                logger.info(f"Frame received: {' '.join(f'{byte:02X}' for byte in buffer[:-2])}")
                                
                                if self.mcb_return_mode == MCBDataReturnMode.RUN:
                                    payload = buffer[2:-2]
                                    parsed = mcb_run_data_parser(payload)
                                    logger.info(f"Parsed data: {parsed}")
                                    if parsed:
                                        self.rundata_received.emit(parsed)
                                
                                if self.mcb_return_mode == MCBDataReturnMode.SET:
                                    payload = buffer[2:-2]
                                    parsed = mcb_set_data_parser(payload)
                                    logger.info(f"Parsed data: {parsed}")
                                    if parsed:
                                        self.setdata_received.emit(parsed)
                                        self.cfg_return_mode("RUN")

                                
                                # Start new frame with the new start sequence
                                buffer = bytearray()
                            else:
                                # Start of the first frame
                                frame_active = True
                        elif frame_active:
                            # Continue collecting bytes for the current frame
                            continue
                    else:
                        logger.error(f"Could not open port {self.serial_port}")
                        self.stop()
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            self.stop()
            
    def start(self, port_name):
        self.serial_port = port_name
        if not self.thread.isRunning():
            self.thread.start()
    
    def stop(self):
        self.running_ = False
        self.serial_port = None
        if self.serial and self.serial.is_open:
            logger.info("Closing serial port")
            self.serial.close()
            self.serial = None
        
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
        
        self.port_connection_changed.emit(False)
    
    def _send_cmd_to_config_reg16(self, reg, value):
        txdata = [
            MCB_MSG_H1, 
            MCB_MSG_H2, 
            0x06,
            MCB_MSG_TX_CMD, 
            (reg >> 8) & 0xFF,
            reg & 0xFF,
            0x01,
            (value >> 8) & 0xFF,
            value & 0xFF
        ]
        with self.serial_lock:
            self.serial.write(bytearray(txdata))
        
    def _send_cmd_to_set_return_mode(self, mode):
        if mode == MCBDataReturnMode.RUN:
            self._send_cmd_to_config_reg16(mcb_regs.MCB_DATA_MODE_REG, 0)
        elif mode == MCBDataReturnMode.SET:
            self._send_cmd_to_config_reg16(mcb_regs.MCB_DATA_MODE_REG, 1)
            
            
    def cfg_return_mode(self, mode):
        logger.info(f"Setting return mode to {mode}")
        if mode == "RUN":
            self.mcb_return_mode = MCBDataReturnMode.RUN
            self._send_cmd_to_set_return_mode(MCBDataReturnMode.RUN)
        elif mode == "SET":
            self.mcb_return_mode = MCBDataReturnMode.SET
            self._send_cmd_to_set_return_mode(MCBDataReturnMode.SET)
        logger.info(f"Return mode set to {mode}")
            
    
    def on_reg16_new_config(self, cfg):
        self._send_cmd_to_config_reg16(cfg["reg"], cfg["val"])
        # self.cfg_return_mode("SET") # Lock not working --> TODO: Fix this
    
    
        
