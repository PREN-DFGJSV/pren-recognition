from src.model.CubePart import CubePart
from src.enums.EOrientierung import EOrientierung
from src.enums.EColor import EColor
from src.turntable_alignment.TurntableQuadrantStream import TurntableQuadrantStream
from src.common.ConfigProperties import ConfigProperties
from src.communication import DbContext, WebServer
from src.services.ValidationService import ValidationService
from src.model.BuildInstructionDto import BuildInstructionDto
from typing import List

config = ConfigProperties()


class RecognitionService:
    
    @staticmethod
    def analyze_turntable_video_stream():
        print("Starting analyzing turntable.", flush=True)

        db = DbContext.SQLiteDB("results.db")
        db.reset_table()

        frames = TurntableQuadrantStream().detect_aligned_frames()

        if frames is None or len(frames) == 0:
            print("No frames found!", flush=True)
            return

        RecognitionService.get_build_instructions_from_db(3, db)
            
        # Wait for continue
        if (not config.DEPLOY_ENV_PROD):
            input("Press Enter to continue...")

    @staticmethod
    def get_build_instructions_from_db(instruction_no: int, db_context: DbContext.SQLiteDB) -> List[List[BuildInstructionDto]]:
        recognition_results = db_context.get_recognitions_by_max_id(instruction_no)
        instructions_list = []

        built_pattern = [
            None, None, None, None,
            None, None, None, None,
        ]

        built_pattern_debug = [
            None, None, None, None,
            None, None, None, None,
        ]

        recognized_pattern = [
            None, None, None, None,
            None, None, None, None,
        ]

        recognized_pattern_debug = [
            None, None, None, None,
            None, None, None, None,
        ]

        # Alle instruktionen werden nach aktuellem Stand rekonstruiert
        for recognition_result in recognition_results:
            instructions = []
            for pos, color in recognition_result.items():
                if pos == 'id':  # Überspringen der id-Spalte
                    continue
                if color is not None:
                    position = int(pos.replace("pos", ""))
                    pos = position - 1

                    # Check if this cube is recognized for the first time   
                    if recognized_pattern[pos] is None:
                        print("Cube at pos", pos + 1, "detected with color", int(color))
                        recognized_pattern[pos] = BuildInstructionDto(position, int(color))
                        recognized_pattern_debug[pos] = color
                            
                        # Check if lower layer
                        if position < 5:
                            built_pattern[pos] = recognized_pattern[pos]
                            built_pattern_debug[pos] = color
                            instructions.append(built_pattern[pos])

                            # If it fills overhang then also append the overhang to the instruction
                            if recognized_pattern[pos + 4] is not None:
                                built_pattern[pos + 4] = recognized_pattern[pos + 4]
                                built_pattern_debug[pos + 4] = recognized_pattern[pos + 4].color
                                instructions.append(built_pattern[pos + 4])

                        # Check if lower layer was built to place upper
                        elif built_pattern[pos - 4] is not None:
                            built_pattern[pos] = recognized_pattern[pos]
                            built_pattern_debug[pos] = color
                            instructions.append(built_pattern[pos])

            print("Recog pattern:", recognized_pattern_debug)
            print("Built pattern:", built_pattern_debug)

            instructions_list.append(instructions)

        # TODO-go: Usefull/needed?
        # Überprüfen, ob alle Positionsspalten nicht NULL sind
        # all_positions_filled = all(value is not None for key, value in current_result.items() if key.startswith('pos'))

        return instructions_list

    # TODO: Remove
    @staticmethod
    def test_fill_with_static_data_variation_a():

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

    @staticmethod
    def test_fill_with_static_data_variation_b():

        db = DbContext.SQLiteDB("results.db")

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

    @staticmethod
    def test_reading_instructions():

        db = DbContext.SQLiteDB(ConfigProperties.DATABASE_NAME)
        print("First instruction")
        WebServer.get_build_instructions_from_db(1, db)

        print("Second instruction")
        WebServer.get_build_instructions_from_db(2, db)

        print("Third and final instruction")
        WebServer.get_build_instructions_from_db(3, db)

        ValidationService.send_to_validation_server("2024-08-13 11:44:00")

        # Wait for continue
        if (not config.DEPLOY_ENV_PROD):
            input("Press Enter to continue...")