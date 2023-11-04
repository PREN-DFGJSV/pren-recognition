import numpy as np

from src.common.constants import *
from src.enums.EColor import EColor


class ColorHelper:
    @staticmethod
    def __is_within_range(value, lower_bound, upper_bound):
        return np.all(lower_bound <= value) and np.all(value <= upper_bound)

    @staticmethod
    def get_color(hsv_value) -> EColor:
        if ColorHelper.__is_within_range(hsv_value, LOWER_RED, UPPER_RED):
            return EColor.RED
        elif ColorHelper.__is_within_range(hsv_value, LOWER_YELLOW, UPPER_YELLOW):
            return EColor.YELLOW
        elif ColorHelper.__is_within_range(hsv_value, LOWER_BLUE, UPPER_BLUE):
            return EColor.BLUE
        elif ColorHelper.__is_within_range(hsv_value, LOWER_WHITE, UPPER_WHITE):
            return EColor.WHITE
        elif ColorHelper.__is_within_range(hsv_value, LOWER_BLACK, UPPER_BLACK):
            return EColor.BLACK
        else:
            return EColor.UNDEFINED
