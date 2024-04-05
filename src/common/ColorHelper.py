import numpy as np

from src.enums.EColor import EColor
from src.common.ConfigProperties import ConfigProperties

config = ConfigProperties()


class ColorHelper:
    @staticmethod
    def __is_within_range(value, lower_bound, upper_bound):
        return np.all(lower_bound <= value) and np.all(value <= upper_bound)

    @staticmethod
    def get_color(hsv_value) -> EColor:
        if ColorHelper.__is_within_range(hsv_value, config.LOWER_RED, config.UPPER_RED):
            return EColor.RED
        elif ColorHelper.__is_within_range(hsv_value, config.LOWER_YELLOW, config.UPPER_YELLOW):
            return EColor.YELLOW
        elif ColorHelper.__is_within_range(hsv_value, config.LOWER_BLUE, config.UPPER_BLUE):
            return EColor.BLUE
        elif ColorHelper.__is_within_range(hsv_value, config.LOWER_WHITE, config.UPPER_WHITE):
            return EColor.WHITE
        elif ColorHelper.__is_within_range(hsv_value, config.LOWER_BLACK, config.UPPER_BLACK):
            return EColor.BLACK
        else:
            return EColor.UNDEFINED
