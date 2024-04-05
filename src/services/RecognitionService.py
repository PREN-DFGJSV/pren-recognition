import cv2

from src.color_recognition.ColorRecognizer import ColorRecognizer
from src.common.CubeHelper import CubeHelper
from src.enums.EOrientierung import EOrientierung
from src.turntable_alignment.TurntableQuadrantStream import TurntableQuadrantStream


class RecognitionService:
    
    @staticmethod
    def analyze_turntable_video_stream():
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