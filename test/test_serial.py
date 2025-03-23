import serial


serial_port = serial.Serial(port="/dev/ttyUSB0", baudrate=115200)
if serial_port.is_open:
    print("Port is open")
    while True:
        data = serial_port.readline()
        print(f"Received: {data}")
else:
    print("Could not open port")
    serial_port.close()
    serial_port = None

