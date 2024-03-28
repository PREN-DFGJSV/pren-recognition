from src.model.BaseDto import BaseDto
import json


class BuildInstructionDto(BaseDto):
    def __init__(self, position: int, color: int, is_finished: bool):
        self.position = position
        self.color = color
        self.is_finished = is_finished

    def to_json(self):
        """
        Konvertiert das Objekt in ein JSON-String.
        :return: Eine String-Repräsentation des Objekts im JSON-Format.
        """
        return json.dumps({
            "position": self.position,
            "color": self.color,
            "is_finished": self.is_finished
        }, indent=2)
