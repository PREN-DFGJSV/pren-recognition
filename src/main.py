from datetime import datetime

import cv2

from src.color_recognition.ColorRecognizer import ColorRecognizer
from src.common.ColorHelper import ColorHelper
from src.common.CubeHelper import CubeHelper
from src.common.constants import *
from src.communication.HttpClient import HttpClient
from src.enums.EOrientierung import EOrientierung
from src.model.CubePart import CubePart
from src.model.ResultDto import ResultDto
from src.turntable_alignment.TurntableQuadrant import TurntableQuadrant

if __name__ == "__main__":
    print("Start Programm...")

    # Bilder aus Video auslesen
    turntable = TurntableQuadrant("res/XGGR_XXRX.mp4", rpm = 2)
    frames = turntable.detect_aligned_frames()

    for frame in frames:
        cv2.imshow("Detected frame", frame.debug_frame)
        cv2.waitKey(0)

    # Bild 1 Farben auslesen
    cr1 = ColorRecognizer(cv2.imread("res/BGGR_RBRB/NORTH.png"))
    farbe1 = cr1.get_avg_color_from_area(MESSPUNKT_OBEN_LINKS)
    farbe2 = cr1.get_avg_color_from_area(MESSPUNKT_OBEN_RECHTS)
    farbe3 = cr1.get_avg_color_from_area(MESSPUNKT_UNTEN_LINKS)
    farbe4 = cr1.get_avg_color_from_area(MESSPUNKT_UNTEN_RECHTS)

    # Bild 2 Farben auslesen
    cr2 = ColorRecognizer(cv2.imread("res/BGGR_RBRB/SOUTH.png.png"))
    farbe5 = cr2.get_avg_color_from_area(MESSPUNKT_OBEN_LINKS)
    farbe6 = cr2.get_avg_color_from_area(MESSPUNKT_OBEN_RECHTS)
    farbe7 = cr2.get_avg_color_from_area(MESSPUNKT_UNTEN_LINKS)
    farbe8 = cr2.get_avg_color_from_area(MESSPUNKT_UNTEN_RECHTS)

    # Merge Cube
    part1 = CubePart(orientierung=EOrientierung.NORD,
                     unten_links=ColorHelper.get_color(farbe1),
                     unten_rechts=ColorHelper.get_color(farbe2),
                     oben_links=ColorHelper.get_color(farbe3),
                     oben_rechts=ColorHelper.get_color(farbe4))

    part2 = CubePart(orientierung=EOrientierung.SUED,
                     unten_links=ColorHelper.get_color(farbe5),
                     unten_rechts=ColorHelper.get_color(farbe6),
                     oben_links=ColorHelper.get_color(farbe7),
                     oben_rechts=ColorHelper.get_color(farbe8))

    cube = CubeHelper.merge_cube_part_to_cube(part1, part2)

    # Übermitteln
    server = HttpClient("https://google.ch/test")
    result = server.post_dto(ResultDto.from_cube(datetime.now(), cube))

    print(f"Der Webserver lieferte den HTTP-Statuscode {result}")

    print("End Programm...")
