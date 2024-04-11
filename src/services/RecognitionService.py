from src.color_recognition.ColorRecognizer import ColorRecognizer
from src.common.CubeHelper import CubeHelper
from src.enums.EOrientierung import EOrientierung
from src.turntable_alignment.TurntableQuadrantStream import TurntableQuadrantStream
from src.common.ConfigProperties import ConfigProperties

config = ConfigProperties()


class RecognitionService:
    
    @staticmethod
    def analyze_turntable_video_stream():
        print("Starting analyzing turntable.", flush=True)

        frames = TurntableQuadrantStream().detect_aligned_frames()

        if frames is None or len(frames) == 0:
            print("No frames found!", flush=True)
            return
        
        # Wait for continue
        if (not config.DEPLOY_ENV_PROD):
            input("Press Enter to continue...")

        # Bild 1 Farben auslesen
        # cr_first = ColorRecognizer(frames[0].frame, frames[0].orientation)
        # cr_third = ColorRecognizer(frames[2].frame, frames[2].orientation)

        # cube = CubeHelper.merge_cube_part_to_cube(cr_first.get_cube_part(), cr_third.get_cube_part())