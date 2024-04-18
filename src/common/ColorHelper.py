import numpy as np

from src.enums.EColor import EColor
from src.common.ConfigProperties import ConfigProperties

config = ConfigProperties()


class ColorHelper:
    @staticmethod
    def get_color(bgr_value: tuple) -> EColor:
        # Farbkanäle extrahieren
        b, g, r = bgr_value

        # Farbnamen basierend auf den Farbwerten bestimmen
        if b > 200 and g < 100 and r < 100:
            return EColor.BLUE
        elif b < 100 and g > 200 and r > 200:
            return EColor.YELLOW
        elif b < 100 and g < 100 and r > 200:
            return EColor.RED
        else:
            return EColor.UNDEFINED
