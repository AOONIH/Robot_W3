# import the necessary packages
import argparse
import imutils
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import serial
from control import control_motor

from find_ball import find_red, find_blue, find_green

# construct the argument parse and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument("--novideo", action="store_true")
args = parser.parse_args()

camera = PiCamera()  # PiCamera object
camera.resolution = (640, 480)
camera.framerate = 30
window_size = 600
buffer = PiRGBArray(camera)  # PiRGBArray object
time.sleep(0.1)  # 100ms

running = True
con = serial.Serial("/dev/ttyACM0", 9600)
con.write(b"I")
while running:
    for stream in camera.capture_continuous(buffer, format="bgr", use_video_port=True):

        frame = stream.array
        frame = imutils.resize(frame, width=window_size)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        red_center = find_red(hsv)
        blue_center = find_blue(hsv)
        green_center = find_green(hsv)
        control_motor(con, green_center, red_center, window_size)

        if not args.novideo:
            if red_center:
                cv2.circle(frame, red_center, 5, (0, 0, 255), -1)
            if blue_center:
                cv2.circle(frame, blue_center, 5, (255, 0, 0), -1)
            if green_center:
                cv2.circle(frame, green_center, 5, (0, 255, 0), -1)
            cv2.imshow("Frame", frame)

        stream.truncate(0)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    running = False
cv2.destroyAllWindows()
