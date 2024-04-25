from enum import Enum


class EValidationResult(Enum):
    OK = 200
    NO_CONTENT = 204
    UNAUTHORIZED = 401
    METHOD_NOT_ALLOWED = 405
    MEDIA_TYPE_NOT_SUPPORTED = 415
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500

    @staticmethod
    def from_int(value: int):
        for enum_value in EValidationResult:
            if enum_value.value == value:
                return enum_value
        raise ValueError(f"Ungültiger Wert für EValidationResult: {value}")
