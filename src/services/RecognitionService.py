from src.model.CubePart import CubePart
from src.enums.EOrientierung import EOrientierung
from src.enums.EColor import EColor
from src.turntable_alignment.TurntableQuadrantStream import TurntableQuadrantStream
from src.common.ConfigProperties import ConfigProperties
from src.communication import DbContext, WebServer

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
    def test_fill_with_static_data():

        db = DbContext.SQLiteDB("results.db")

        # Initial state, orientation facing north, rotating clockwise
        # II | I       | G       | R  
        # ---+---   ---+---   ---+---
        # III| IV    B |         |   

        db.reset_table()

        cubePart1: CubePart = CubePart(EOrientierung.NORD, EColor.BLUE, EColor.UNDEFINED, EColor.UNDEFINED, EColor.RED)
        db.insert_cube_part(cubePart1) # p3: B, p5: R

        cubePart2: CubePart = CubePart(EOrientierung.WEST, EColor.UNDEFINED, EColor.YELLOW, EColor.UNDEFINED, EColor.UNDEFINED)
        db.insert_cube_part(cubePart2) # p1: Y

        cubePart3: CubePart = CubePart(EOrientierung.SUED, EColor.YELLOW, EColor.UNDEFINED, EColor.UNDEFINED, EColor.UNDEFINED)
        db.insert_cube_part(cubePart3) # p1: Y

        cubePart4: CubePart = CubePart(EOrientierung.OST, EColor.UNDEFINED, EColor.BLUE, EColor.RED, EColor.UNDEFINED)
        db.insert_cube_part(cubePart4) # p3: B, p5: R

        # Initial state, orientation facing west, rotating clockwise
        # III| II    G | R     G | R  
        # ---+---   ---+---   ---+---
        # IV |  I    B |       B |   

        db.reset_table()
        
        cubePart1: CubePart = CubePart(EOrientierung.WEST, EColor.BLUE, EColor.UNDEFINED, EColor.YELLOW, EColor.RED)
        db.insert_cube_part(cubePart1) # p4: B, p6: R, p7: G

        cubePart2: CubePart = CubePart(EOrientierung.SUED, EColor.UNDEFINED, EColor.RED, EColor.BLUE, EColor.YELLOW)
        db.insert_cube_part(cubePart2) # p2: R, p7: G, p8: B

        cubePart3: CubePart = CubePart(EOrientierung.OST, EColor.RED, EColor.YELLOW, EColor.UNDEFINED, EColor.BLUE)
        db.insert_cube_part(cubePart3) # p2: R, p3: Y, p8: B

        cubePart4: CubePart = CubePart(EOrientierung.NORD, EColor.YELLOW, EColor.BLUE, EColor.RED, EColor.UNDEFINED)
        db.insert_cube_part(cubePart4) # p3: Y, p4: B, p6: R

        # Wait for continue
        if (not config.DEPLOY_ENV_PROD):
            input("Press Enter to continue...")

    @staticmethod
    def test_reading_instructions():

        db = DbContext.SQLiteDB("results.db")
        print(WebServer.get_build_instructions_from_db(2, db))

        # Wait for continue
        if (not config.DEPLOY_ENV_PROD):
            input("Press Enter to continue...")