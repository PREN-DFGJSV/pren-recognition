from dataclasses import dataclass

from src.enums.EOrientierung import EOrientierung
from src.enums.EColor import EColor


class CubePart:
    orientierung: EOrientierung

    unten_links: EColor = EColor.UNDEFINED
    unten_rechts: EColor = EColor.UNDEFINED
    oben_links: EColor = EColor.UNDEFINED
    oben_rechts: EColor = EColor.UNDEFINED

    pos1: EColor = EColor.UNDEFINED
    pos2: EColor = EColor.UNDEFINED
    pos3: EColor = EColor.UNDEFINED
    pos4: EColor = EColor.UNDEFINED
    pos5: EColor = EColor.UNDEFINED
    pos6: EColor = EColor.UNDEFINED
    pos7: EColor = EColor.UNDEFINED
    pos8: EColor = EColor.UNDEFINED

    def __init__(self, orientierung: EOrientierung, unten_links: EColor, unten_rechts: EColor, oben_links: EColor, oben_rechts: EColor):
        
        self.unten_links = unten_links
        self.unten_rechts = unten_rechts
        self.oben_links = oben_links
        self.oben_rechts = oben_rechts
            
        self.__translate_positions(orientierung, unten_links, unten_rechts, oben_links, oben_rechts)

    def __translate_positions(self, orientierung: EOrientierung, unten_links: EColor, unten_rechts: EColor, oben_links: EColor, oben_rechts: EColor) -> None:
    
        orientierung_offset = orientierung.value + 1
        layer2_offset = 4

        unten_links_pos: int = (orientierung_offset) % layer2_offset
        unten_rechts_pos: int = (orientierung_offset + 1) % layer2_offset
        oben_rechts_pos: int = (orientierung_offset + 2) % layer2_offset + layer2_offset
        oben_links_pos: int = (orientierung_offset + 3) % layer2_offset + layer2_offset

        self.__set_pos_color(unten_links_pos, unten_links)
        self.__set_pos_color(unten_rechts_pos, unten_rechts)
        self.__set_pos_color(oben_rechts_pos, oben_rechts)
        self.__set_pos_color(oben_links_pos, oben_links)

    def __set_pos_color(self, pos: int, color: EColor) -> None:
        match pos:
            case 0:
                self.pos1 = color
            case 1:
                self.pos2 = color
            case 2:
                self.pos3 = color
            case 3:
                self.pos4 = color
            case 4:
                self.pos5 = color
            case 5:
                self.pos6 = color
            case 6:
                self.pos7 = color
            case 7:
                self.pos8 = color
            case _:
                print("Unmapped color position in pattern translation!", flush=True)

    def __str__(self):
        return f"CubePart(Orientierung: {self.orientierung.name}, " \
               f"Unten Links: {self.unten_links.name}, " \
               f"Unten Rechts: {self.unten_rechts.name}, " \
               f"Oben Links: {self.oben_links.name}, " \
               f"Oben Rechts: {self.oben_rechts.name})"
    
    def to_key_value_pair(self):
        return {
            "pos1": self.pos1.value if self.pos1.value > 0 else None,
            "pos2": self.pos2.value if self.pos2.value > 0 else None,
            "pos3": self.pos3.value if self.pos3.value > 0 else None,
            "pos4": self.pos4.value if self.pos4.value > 0 else None,
            "pos5": self.pos5.value if self.pos5.value > 0 else None,
            "pos6": self.pos6.value if self.pos6.value > 0 else None,
            "pos7": self.pos7.value if self.pos7.value > 0 else None,
            "pos8": self.pos8.value if self.pos8.value > 0 else None
        }
