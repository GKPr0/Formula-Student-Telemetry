import serial


if __name__ == "__main__":
    ser = serial.Serial()
    ser.baudrate = 1000000
    ser.port = 'COM4'

    ser.open()

    while True:
        print(ser.read_all())