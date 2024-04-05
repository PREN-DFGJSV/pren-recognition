import cv2

from datetime import datetime

from src.common.VideoStream import VideoStream
from src.color_recognition.ColorRecognizer import ColorRecognizer
from src.common.CubeHelper import CubeHelper
from src.communication.HttpClient import HttpClient
from src.enums.EOrientierung import EOrientierung
from src.model.ResultDto import ResultDto
from src.turntable_alignment.TurntableQuadrantStream import TurntableQuadrantStream
from src.common.ConfigProperties import ConfigProperties

config = ConfigProperties()


# TODO: Add debug main with debug visualization & adjustment for parameters, cleanup main
if __name__ == "__main__":

    print(f"[{'PROD' if config.DEPLOY_ENV_PROD else 'DEV'}] Start Programm...")

    # Bilder aus Video auslesen
    frames = TurntableQuadrantStream().detect_aligned_frames()

    if frames is None or len(frames) == 0:
        print("No frames found!")
    else:
        for frame in frames:
            if frame is not None:
                cv2.imshow(f"Detected frame ({frame.orientation})", frame.debug_frame)

    # Bild 1 Farben auslesen
    cr_nord = ColorRecognizer(cv2.imread("res/BGGR_RBRB/NORTH.png"), EOrientierung.NORD)
    cr_sued = ColorRecognizer(cv2.imread("res/BGGR_RBRB/SOUTH.png"), EOrientierung.SUED)

    cube = CubeHelper.merge_cube_part_to_cube(cr_nord.get_cube_part(), cr_sued.get_cube_part())

    # Übermitteln
    server = HttpClient("https://google.ch/test")
    result = server.post_dto(ResultDto.from_cube(datetime.now(), cube))

    print(f"Der Webserver lieferte den HTTP-Statuscode {result}")

    print("End Programm...")
