
import serial.tools.list_ports

# # Get a list of available serial ports
# ports = serial.tools.list_ports.comports()

# # Print each available port
# for port in ports:
#     print(f"Device: {port.device}, Description: {port.description}")

[print(f"Device: {port.device}, Description: {port.description}") for port in serial.tools.list_ports.comports() if "USB" in port.device]


