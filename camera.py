import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np

camera = PiCamera() # PiCamera object
camera.resolution = (640 , 480)
camera.framerate = 30
buffer = PiRGBArray(camera) # PiRGBArray object
time.sleep(0.1) # 100ms

running = True

red_hue = np.array([[170,50,50],[180,255,255]])
green_hue = np.array([[50,50,50],[70,255,255]])
blue_hue = np.array([[110,50,50],[130,255,255]])

while running:
    # capture frames from the camera
    for frame in camera.capture_continuous(buffer, format="bgr", use_video_port=True):
        # store the array attribute of the frame object
        image = cv2.cvtColor(frame.array,cv2.COLOR_BGR2HSV)
        R_masked = cv2.inRange(image,red_hue[0],red_hue[1]) #+ cv2.inRange(image,redN_hue[0],redN_hue[1])
        G_masked = cv2.inRange(image,green_hue[0],green_hue[1]) 
        # show the frame
        cv2.imshow("green",G_masked)
        cv2.imshow('red',R_masked)
        # waits 1ms for a key event, masks everything except the least significant byte
        key = cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame
        frame.truncate(0)

        # if the `q` key was pressed,
        # break out of the for and exit the while
        if key == ord("q"):
            break
    running = False
cv2.destroyAllWindows()
