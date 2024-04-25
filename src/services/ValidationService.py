from src.communication import DbContext
from src.communication.HttpClient import HttpClient
from src.enums.EValidationResult import EValidationResult
from src.model.ResultDto import ResultDto
from src.common.ConfigProperties import ConfigProperties


class ValidationService:
    @staticmethod
    def send_to_validation_server(duration) -> EValidationResult:
        db = DbContext.SQLiteDB(f'../communication/{ConfigProperties.DATABASE_NAME}')
        db_result = db.get_recognition_by_id(db.get_max_id())

        formatted_dict = {key: (value if value is not None else '') for key, value in db_result.items()}
        result_dto = ResultDto(duration, formatted_dict)

        url = f'{ConfigProperties.VALIDATION_URL}/cubes/{ConfigProperties.VALIDATION_TEAM_ID}'
        http_client = HttpClient(url, ConfigProperties.VALIDATION_TOKEN)

        http_result = http_client.post_dto(result_dto)

        return EValidationResult.from_int(http_result)

