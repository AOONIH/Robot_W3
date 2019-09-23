import serial
import time

if __name__ == "__main__":
    con = serial.Serial("/dev/ttyACM0", 9600)
    while(True):
        con.write("F")
        time.sleep(1)
        con.write("B")
        time.sleep(1)
