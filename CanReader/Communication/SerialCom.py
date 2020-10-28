# !/usr/bin/python3

import serial
import time

if __name__ == "__main__":

    ser = serial.Serial('COM4', 921600, timeout=None) #921600 buad is max speed of cp2102

    startTime = time.time()
    i = 0
    while i < 125000:
        i += len(ser.read(ser.inWaiting())) # 1.35 sec on 1Mbit
    print(time.time() - startTime)