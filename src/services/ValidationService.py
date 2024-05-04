from src.communication import DbContext
from src.communication.HttpClient import HttpClient
from src.enums.EValidationResult import EValidationResult
from src.model.ResultDto import ResultDto
from src.common.ConfigProperties import ConfigProperties


class ValidationService:
    @staticmethod
    def send_to_validation_server(duration) -> EValidationResult:
        db = DbContext.SQLiteDB(ConfigProperties.DATABASE_NAME)

        result_dto = ValidationService.get_recognized_pattern_from_db(db, duration)

        url = f'{ConfigProperties.VALIDATION_URL}/cubes/{ConfigProperties.VALIDATION_TEAM_ID}/config'
        http_client = HttpClient(url, ConfigProperties.VALIDATION_TOKEN)

        http_result = http_client.post_dto(result_dto)
        return EValidationResult.from_int(http_result)
    
    @staticmethod
    def get_recognized_pattern_from_db(db_context: DbContext.SQLiteDB, duration) -> ResultDto:
        db_result = db_context.get_recognitions_by_max_id(3)

        result_dto = ResultDto(duration)
        recognized_pattern = [
            None, None, None, None,
            None, None, None, None,
        ]

        # Alle instruktionen werden nach aktuellem Stand rekonstruiert
        for recognition_result in db_result:
            for pos, color in recognition_result.items():
                if pos == 'id':  # Überspringen der id-Spalte
                    continue
                if color is not None:
                    position = int(pos.replace("pos", ""))
                    pos = position - 1

                    # Check if this cube is recognized for the first time   
                    if recognized_pattern[pos] is None:
                        print("Cube at pos", pos, "detected")
                        colorString = "blue"

                        match int(color):
                            case 2:
                                colorString = "red"
                            case 3:
                                colorString = "yellow"
                            case _:
                                print("Unknown color found in recognized pattern", flush=True)

                        recognized_pattern[pos] = colorString
                        result_dto.set_config_value(pos, colorString)

        print("Full recognized pattern:", recognized_pattern)
        return result_dto

