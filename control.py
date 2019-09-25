from collections import deque
import logging

logger = logging.getLogger()

class Controller:

    def __init__(self, num_green, window_width):
        self.num_green = num_green
        self.chase_green = True
        self.last_radious = deque
        self.window_width = window_width
        self.captures = False
        self.green_pop_count = 0
        self.key = "green"

    def control(self, con, center_info):
        self.control_motor(con, center_info[self.key])
        if self.key == "green":
            self.pop_detection(con, center_info["green"][1])

    def pop_detection(self, con, radius):
        if (not self.captures) and radius > self.window_width*0.5:
            self.captures = True
            logger.critical("balloon captured")

        if self.captures and radius < self.window_width*0.5:
            # poped
            self.captures = False
            self.green_pop_count += 1
            logger.critical("balloon poped")

    def control_motor(self, con, center):
        if center is None:
            con.write(b"S")
            return False
        elif center[0] < self.window_width * 0.3:
            con.write(b"L")
            return False
        elif center[0] > self.window_width * 0.7:
            con.write(b"R")
            return False
        else:
            con.write(b"F")
            return True
