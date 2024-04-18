import string
from dataclasses import dataclass

from src.enums.EOrientierung import EOrientierung
from src.enums.EColor import EColor


@dataclass
class CubePart:
    orientierung: EOrientierung
    unten_links: EColor
    unten_rechts: EColor
    oben_links: EColor
    oben_rechts: EColor

    def __str__(self):
        return f"CubePart(Orientierung: {self.orientierung.name}, " \
               f"Unten Links: {self.unten_links.name}, " \
               f"Unten Rechts: {self.unten_rechts.name}, " \
               f"Oben Links: {self.oben_links.name}, " \
               f"Oben Rechts: {self.oben_rechts.name})"
