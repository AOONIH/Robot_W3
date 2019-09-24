import cv2
import imutils

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
redLower = (170, 86, 6)
redUpper = (180, 255, 255)
blueLower = (110, 30, 6)
blueUpper = (130, 255, 255)

def find_red(hsv):
    return find_ball(hsv, redLower, redUpper)

def find_blue(hsv):
    return find_ball(hsv, blueLower, blueUpper)

def find_green(hsv):
    return find_ball(hsv, greenLower, greenUpper)


def find_ball(hsv, lower_color, upper_color):
    mask = cv2.inRange(hsv, lower_color, upper_color)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        centre = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 10:
            return centre
        else:
            return None
