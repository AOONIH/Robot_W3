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
        self.pop_until = None
        self.recent_pop = 0
        self.key = "green"

    def control(self, con, center_info):
        self.control_motor(con, center_info[self.key][0])
        if self.key == "green":
            self.pop_detection(con, center_info["green"][1])

    def pop_detection(self, con, radius):
        if radius is None:
            radius = 0.0

        if (self.pop_until is not None and self.pop_until > time.time()):
            self.captures = False

        if (not self.captures) and radius > self.window_width*0.4:
            self.captures = True
            self.pop_until = time.time() + 3
            logger.critical("balloon captured")

        if self.captures and radius < self.window_width*0.1:
            # poped
            self.captures = False
            self.green_pop_count += 1
            self.recent_pop = time.time()
            logger.critical("balloon poped")

    def control_motor(self, con, center):
        if center is None:
            if(self.recent_pop + 10 < time.time()):
                con.write(b"S")
            else:
                con.write(b"R")
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
