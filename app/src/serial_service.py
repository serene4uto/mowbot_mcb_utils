
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
import serial
from ctypes import c_ubyte
from app.src.logger import logger

from app.src.mcb import (
    MCBDataReturnMode,
    mcb_data_parser
)
        
class SerialService(QObject):
    
    port_connection_changed = pyqtSignal(bool)
    rundata_received = pyqtSignal(dict)
    
    
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
                                    parsed = mcb_data_parser(payload, self.mcb_return_mode)
                                    logger.info(f"Parsed data: {parsed}")
                                    if parsed:
                                        self.rundata_received.emit(parsed)
                                
                                if self.mcb_return_mode == MCBDataReturnMode.SET:
                                    pass

                                
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