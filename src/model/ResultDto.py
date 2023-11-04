import json
import string
from datetime import datetime

from src.model.BaseDto import BaseDto
from src.model.Cube import Cube


class ResultDto(BaseDto):
    def __init__(self, time_str: string, config=None):
        """
        Initialisiert das ConfigObject mit einem Zeitstempel und einer Konfiguration.
        :param time_str: Zeitstempel als String im Format "YYYY-MM-DD HH:MM:SS".
        :param config: Ein Wörterbuch, das die Konfiguration enthält.
        """
        self.time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        self.config = config if config is not None else {}

    @classmethod
    def from_cube(cls, time_str: string, cube: Cube):
        time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        config = {
            '0': cube.pos1,
            '1': cube.pos2,
            '2': cube.pos3,
            '3': cube.pos4,
            '4': cube.pos5,
            '5': cube.pos6,
            '6': cube.pos7,
            '7': cube.pos8
        }
        return cls(time, config)

    def set_config_value(self, key: string, value: string) -> None:
        """
        Setzt oder aktualisiert den Wert der Konfiguration für den gegebenen Schlüssel.
        :param key: Der Schlüssel in der Konfiguration.
        :param value: Der Wert, der diesem Schlüssel zugeordnet werden soll.
        """
        self.config[str(key)] = value

    def get_config_value(self, key: string) -> string:
        """
        Gibt den Wert der Konfiguration für den gegebenen Schlüssel zurück.
        :param key: Der Schlüssel in der Konfiguration.
        :return: Der Wert des Schlüssels in der Konfiguration oder None, wenn der Schlüssel nicht existiert.
        """
        return self.config.get(str(key))

    def to_json(self) -> string:
        """
        Konvertiert das Objekt in ein JSON-String.
        :return: Eine String-Repräsentation des Objekts im JSON-Format.
        """
        return json.dumps({
            "time": self.time.strftime("%Y-%m-%d %H:%M:%S"),
            "config": self.config
        }, indent=2)
