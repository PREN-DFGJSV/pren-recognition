import numpy as np
import src.config as config

from src.common.ColorHelper import ColorHelper
from src.enums.EOrientierung import EOrientierung
from src.model.CubePart import CubePart


class ColorRecognizer:
    def __init__(self, image: np.array, orientierung: EOrientierung):
        """

        :param image: Das Eingangsbild (OpenCV Bild).
        """
        self.image = image
        self.orientierung = orientierung

    def __get_avg_color_from_area(self, area: tuple) -> tuple:
        """
        Berechnet die durchschnittliche Farbe in einem bestimmten Bereich eines OpenCV-Bildes.

        :param area: Ein Tupel (x_start, y_start, x_end, y_end) mit den Koordinaten des Bereichs.
        :return: Ein Tupel (R, G, B) mit den durchschnittlichen Farbwerten im Bereich.
        """
        # Extrahiere den Bereich aus dem Bild
        x_start, y_start = area
        bereich_bild = self.image[y_start:(y_start + config.SEITENLAENGE_MESSFLAECHE),
                       x_start:(x_start + config.SEITENLAENGE_MESSFLAECHE)]

        # Berechne die durchschnittliche Farbe im Ausschnitt
        avg_color = np.mean(bereich_bild, axis=(0, 1))

        return tuple(map(int, avg_color[::1]))

    def get_cube_part(self) -> CubePart:
        farbe1 = self.__get_avg_color_from_area(config.MESSPUNKT_OBEN_LINKS)
        farbe2 = self.__get_avg_color_from_area(config.MESSPUNKT_OBEN_RECHTS)
        farbe3 = self.__get_avg_color_from_area(config.MESSPUNKT_UNTEN_LINKS)
        farbe4 = self.__get_avg_color_from_area(config.MESSPUNKT_UNTEN_RECHTS)

        return CubePart(orientierung=self.orientierung,
                        unten_links=ColorHelper.get_color(farbe1),
                        unten_rechts=ColorHelper.get_color(farbe2),
                        oben_links=ColorHelper.get_color(farbe3),
                        oben_rechts=ColorHelper.get_color(farbe4))
