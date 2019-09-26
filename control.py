from collections import deque
import logging
import time

logger = logging.getLogger()


class Controller:

    def __init__(self, num_green, window_width):
        self.num_green = num_green
        self.chase_green = True
        self.last_radious = deque
        self.window_width = window_width
        self.captures = False
        self.green_pop_count = 0
        self.pop_until = 0
        self.recent_pop = 0
        self.key = "green"
        self.detected = False
        self.serching_count = 0
        self.last_turn = "R"

    def control(self, con, center_info):
        self.control_motor(con, center_info[self.key][0])
        if self.key == "green":
            self.pop_detection(con, center_info["green"][1])

    def pop_detection(self, con, radius):

        if radius is None:
            radius = 0.0

        if (not self.captures) and radius > self.window_width*0.4:
            self.captures = True
            self.pop_until = 10
            logger.critical("balloon captured")

        if (self.pop_until > 0):
            self.pop_until -= 1
            if self.pop_until == 0:
                self.captures = False

        if self.captures and radius < self.window_width*0.1:
            # poped
            self.captures = False
            self.green_pop_count += 1
            self.detected = False
            logger.critical("balloon poped")

        if self.green_pop_count == self.num_green:
            self.key = "red"

    def control_motor(self, con, center):
        center_threshold = 0.3 * (1.1 ** self.serching_count) 
        if center is None and (not self.detected):
            con.write(b"S")
        elif center is None and self.detected:
            if self.last_turn == "R":
                con.write(b"L")
            else:
                con.write(b"R")
            self.serching_count += 1
        elif center[0] < self.window_width * (0.5 - center_threshold/2):
            con.write(b"L")
            self.detected = True
            self.serching_count = 0
        elif center[0] > self.window_width * (0.5 + center_threshold/2):
            con.write(b"R")
            self.detected = True
            self.serching_count = 0
        else:
            con.write(b"F")
            self.detected = True
            self.serching_count = 0

        if self.serching_count > 7:
            self.serching_count = 0
            self.detected = False
