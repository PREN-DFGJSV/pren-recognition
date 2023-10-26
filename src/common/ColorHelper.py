import numpy as np

# Farbbereiche
LOWER_RED = np.array([0, 50, 50])
UPPER_RED = np.array([10, 255, 255])

LOWER_YELLOW = np.array([22, 93, 0])
UPPER_YELLOW = np.array([45, 255, 255])

LOWER_BLUE = np.array([110, 50, 50])
UPPER_BLUE = np.array([130, 255, 255])

LOWER_WHITE = np.array([0, 200, 0])
UPPER_WHITE = np.array([255, 255, 255])

LOWER_BLACK = np.array([0, 0, 0])
UPPER_BLACK = np.array([180, 255, 40])


class ColorHelper:
    @staticmethod
    def __is_within_range(value, lower_bound, upper_bound):
        return np.all(lower_bound <= value) and np.all(value <= upper_bound)

    @staticmethod
    def get_color(hsv_value):
        if ColorHelper.__is_within_range(hsv_value, LOWER_RED, UPPER_RED):
            return "Red"
        elif ColorHelper.__is_within_range(hsv_value, LOWER_YELLOW, UPPER_YELLOW):
            return "Yellow"
        elif ColorHelper.__is_within_range(hsv_value, LOWER_BLUE, UPPER_BLUE):
            return "Blue"
        elif ColorHelper.__is_within_range(hsv_value, LOWER_WHITE, UPPER_WHITE):
            return "White"
        elif ColorHelper.__is_within_range(hsv_value, LOWER_BLACK, UPPER_BLACK):
            return "Black"
        else:
            return ""
