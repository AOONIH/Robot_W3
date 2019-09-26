# import the necessary packages
import argparse
import imutils
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import serial

import json
import logging
import click
from pathlib import Path

from find_ball import find_red, find_blue, find_green
from control import Controller
from utils.custom_logging import configure_logger


DATA_DIR = Path.cwd().joinpath('data')
SLACK_URL = json.load(Path.cwd().joinpath('config.json').open('r'))['slack']

SCRIPT_NAME = Path(__file__).stem
LOG_DIR = Path.cwd().joinpath(f'logs/{SCRIPT_NAME}')

logger = logging.getLogger()
configure_logger(SCRIPT_NAME, log_dir=LOG_DIR, webhook_url=SLACK_URL)

# construct the argument parse and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument("--novideo", action="store_true")
args = parser.parse_args()

logger.critical("hoge")

camera = PiCamera()  # PiCamera object
camera.resolution = (640, 480)
camera.framerate = 30
window_size = 600
buffer = PiRGBArray(camera)  # PiRGBArray object
num_green = 5
time.sleep(0.1)  # 100ms

running = True
con = serial.Serial("/dev/ttyACM0", 9600)
con.write(b"I")
controller = Controller(num_green, window_size)
while running:
    for stream in camera.capture_continuous(buffer, format="bgr", use_video_port=True):

        frame = stream.array
        frame = imutils.resize(frame, width=window_size)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        hsv = hsv[:-100,:,:]
        red_info = find_red(hsv)
        green_info = find_green(hsv)
        centre_info = dict(red=red_info, green=green_info)
        controller.control(con, centre_info)
        
        if not args.novideo:
            if centre_info["red"][0]:
                cv2.circle(frame, centre_info["red"][0], 5, (0, 0, 255), -1)
            if centre_info["green"][0]:
                cv2.circle(frame, centre_info["green"][0], 5, (0, 255, 0), -1)
            cv2.imshow("Frame", frame)

        stream.truncate(0)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    running = False
cv2.destroyAllWindows()
