import numpy as np

from src.common.constants import SEITENLAENGE_MESSFLAECHE


class ColorRecognizer:
    def __init__(self, image: np.array):
        """

        :param image: Das Eingangsbild (OpenCV Bild).
        """
        self.image = image

    def get_avg_color_from_area(self, area: tuple) -> tuple:
        """
        Berechnet die durchschnittliche Farbe in einem bestimmten Bereich eines OpenCV-Bildes.

        :param area: Ein Tupel (x_start, y_start, x_end, y_end) mit den Koordinaten des Bereichs.
        :return: Ein Tupel (R, G, B) mit den durchschnittlichen Farbwerten im Bereich.
        """
        # Extrahiere den Bereich aus dem Bild
        x_start, y_start = area
        bereich_bild = self.image[y_start:(y_start + SEITENLAENGE_MESSFLAECHE),
                       x_start:(x_start + SEITENLAENGE_MESSFLAECHE)]

        # Berechne die durchschnittliche Farbe im Ausschnitt
        avg_color = np.mean(bereich_bild, axis=(0, 1))

        return tuple(map(int, avg_color[::1]))
