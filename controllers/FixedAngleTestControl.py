import time

import linecar_settings as sets
from .Control import Control

class FixedAngleTestControl(Control):
    def __init__(self):
        self.step = 0
        self.init_time = time.time()
        self.elapsed_time = 0

        self.input_angle = None

    def prepare(self):
        pass

    def get_input_angle(self):
        current_time = time.time()
        self.elapsed_time = current_time - self.init_time
        if self.elapsed_time >= sets.INPUT_TIME:
            self.input_angle = sets.INPUT_ANGLE
        else:
            self.input_angle = 0
        print(self.elapsed_time, self.input_angle)

        return self.input_angle

    def is_finished(self):
        return self.elapsed_time >= sets.ENDING_TIME

    def get_internal_variables(self):
        iv = [self.elapsed_time, self.input_angle]

        return iv
