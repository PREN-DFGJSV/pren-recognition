from src.model.CubePart import CubePart
from src.enums.EOrientierung import EOrientierung
from src.enums.EColor import EColor
from src.turntable_alignment.TurntableQuadrantStream import TurntableQuadrantStream
from src.common.ConfigProperties import ConfigProperties
from src.communication import DbContext

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

    @staticmethod
    def test():
        print("Testing", flush=True)

        db = DbContext.SQLiteDB("results.db")
        db.reset_table()

        cubePart1: CubePart = CubePart(EOrientierung.NORD, EColor.BLUE, EColor.UNDEFINED, EColor.UNDEFINED, EColor.RED)
        db.insert_cube_part(cubePart1)

        cubePart2: CubePart = CubePart(EOrientierung.WEST, EColor.UNDEFINED, EColor.BLUE, EColor.UNDEFINED, EColor.UNDEFINED)
        db.insert_cube_part(cubePart2)

        cubePart3: CubePart = CubePart(EOrientierung.SUED, EColor.YELLOW, EColor.UNDEFINED, EColor.UNDEFINED, EColor.UNDEFINED)
        db.insert_cube_part(cubePart3)

        cubePart4: CubePart = CubePart(EOrientierung.OST, EColor.UNDEFINED, EColor.BLUE, EColor.RED, EColor.UNDEFINED)
        db.insert_cube_part(cubePart4)

        # Wait for continue
        if (not config.DEPLOY_ENV_PROD):
            input("Press Enter to continue...")