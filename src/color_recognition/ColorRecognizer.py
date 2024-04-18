import uuid

import cv2
import numpy as np

from src.common.ColorHelper import ColorHelper
from src.enums.EOrientierung import EOrientierung
from src.model.CubePart import CubePart
from src.common.ConfigProperties import ConfigProperties

config = ConfigProperties()


class ColorRecognizer:
    def __init__(self, image: np.array, orientierung: EOrientierung):
        """

        :param image: Das Eingangsbild (OpenCV Bild).
        """
        self.image = image
        self.orientierung = orientierung
        self.masked_image = self.mask_image()

    def __get_avg_color_from_area(self, area: tuple) -> tuple:
        """
        Berechnet die durchschnittliche Farbe in einem bestimmten Bereich eines OpenCV-Bildes.

        :param area: Ein Tupel (x_start, y_start, x_end, y_end) mit den Koordinaten des Bereichs.
        :return: Ein Tupel (R, G, B) mit den durchschnittlichen Farbwerten im Bereich.
        """
        # Extrahiere den Bereich aus dem Bild
        x_start, y_start = area
        bereich_bild = self.masked_image[y_start:(y_start + config.SEITENLAENGE_MESSFLAECHE),
                        x_start:(x_start + config.SEITENLAENGE_MESSFLAECHE)]

        # Mittelwerte der Farbkanäle berechnen
        avg_color = np.mean(bereich_bild, axis=(0, 1))

        return avg_color

    def get_cube_part(self) -> CubePart:
        farbe1 = self.__get_avg_color_from_area(config.MESSPUNKT_UNTEN_LINKS)
        farbe2 = self.__get_avg_color_from_area(config.MESSPUNKT_UNTEN_RECHTS)
        farbe3 = self.__get_avg_color_from_area(config.MESSPUNKT_OBEN_LINKS)
        farbe4 = self.__get_avg_color_from_area(config.MESSPUNKT_OBEN_RECHTS)

        return CubePart(orientierung=self.orientierung,
                        unten_links=ColorHelper.get_color(farbe1),
                        unten_rechts=ColorHelper.get_color(farbe2),
                        oben_links=ColorHelper.get_color(farbe3),
                        oben_rechts=ColorHelper.get_color(farbe4))

    def mask_image(self):
        img = self.image
        # Bild in HSV-Farbraum konvertieren
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Blau-Maske erstellen
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Gelb-Maske erstellen
        lower_yellow = np.array([20, 50, 50])
        upper_yellow = np.array([40, 255, 255])
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Rot-Masken erstellen
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

        lower_red2 = np.array([170, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

        red_mask = cv2.bitwise_or(red_mask1, red_mask2)

        # Gesamtmaske erstellen
        mask = cv2.bitwise_or(blue_mask, yellow_mask)
        mask = cv2.bitwise_or(mask, red_mask)

        # Gewünschte RGB-Werte für Blau, Gelb und Rot festlegen
        blue_rgb = [255, 0, 0]  # Beispiel: Reines Blau (R=255, G=0, B=0)
        yellow_rgb = [0, 255, 255]  # Beispiel: Reines Gelb (R=0, G=255, B=255)
        red_rgb = [0, 0, 255]  # Beispiel: Reines Rot (R=0, G=0, B=255)

        # Leeres Ergebnisbild erstellen
        result = np.zeros_like(img)

        # Farben im Ergebnisbild durch die gewünschten RGB-Werte ersetzen
        result[blue_mask > 0] = blue_rgb
        result[yellow_mask > 0] = yellow_rgb
        result[red_mask > 0] = red_rgb

        # Ergebnis anzeigen
        if not config.DEPLOY_ENV_PROD and config.DEBUG_SHOW_COLOR_MASK:
            cv2.imshow(f'Masked Frame {uuid.uuid4()}', result)

        return result
