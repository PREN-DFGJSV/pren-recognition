import cv2
import numpy as np


class ColorPair:
    __lower: np.array
    __upper: np.array

    def __init__(self, lower: np.array, upper: np.array):
        self.__lower = lower
        self.__upper = upper

    def get_mask(self, image):
        return cv2.inRange(image, self.__lower, self.__upper)

    @staticmethod
    def build_mask(img, color_maps):
        mask = 0
        for color_pair in color_maps:
            mask += cv2.inRange(img, color_pair.lower, color_pair.upper)
        return mask
