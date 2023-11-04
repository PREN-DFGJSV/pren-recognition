from src.common.CubePartHelper import CubePartHelper
from src.exceptions.BilderOrientierungNichtUnterstuetzt import BilderOrientierungNichtUnterstuetzt
from src.exceptions.FalscheFarbeErkanntException import FalscheFarbeErkanntException
from src.model.CubePart import CubePart
from src.model.Cube import Cube
from src.enums.EOrientierung import EOrientierung


class CubeHelper:
    @staticmethod
    def merge_cube_part_to_cube(first_part: CubePart, second_part: CubePart) -> Cube:
        cube: Cube = Cube()
        wuerfel_farben = ["blue", "yellow", "red"]

        # Prüfung der Orientierung und ausrichten
        if first_part.orientierung is EOrientierung.NORD and second_part.orientierung is EOrientierung.SUED:
            nord_part = first_part
            sued_part = second_part
        elif first_part.orientierung is EOrientierung.SUED and second_part.orientierung is EOrientierung.NORD:
            sued_part = first_part
            nord_part = second_part
            # TODO mach dies oberhalb Sinn auch unten??
        elif first_part.orientierung is EOrientierung.OST and second_part.orientierung is EOrientierung.WEST:
            nord_part, sued_part = CubePartHelper.change_cube_part_orientation(first_part, second_part)
        elif first_part.orientierung is EOrientierung.WEST and second_part.orientierung is EOrientierung.OST:
            nord_part, sued_part = CubePartHelper.change_cube_part_orientation(second_part, first_part)
        else:
            raise BilderOrientierungNichtUnterstuetzt("Diese Orientierungskombination wird nicht unterstützt.")

        # Unterer Layer
        cube.pos1 = nord_part.unten_links
        cube.pos2 = nord_part.unten_rechts
        cube.pos3 = sued_part.unten_links
        cube.pos4 = sued_part.unten_rechts

        # Oberer Layer
        if cube.pos1 in wuerfel_farben:
            cube.pos5 = sued_part.oben_rechts
        else:
            raise FalscheFarbeErkanntException("Falsche Farbe an der Position 1/5 erkannt")

        if cube.pos2 in wuerfel_farben:
            cube.pos6 = sued_part.oben_links
        else:
            raise FalscheFarbeErkanntException("Falsche Farbe an der Position 2/6 erkannt")

        if cube.pos3 in wuerfel_farben:
            cube.pos7 = nord_part.oben_rechts
        else:
            raise FalscheFarbeErkanntException("Falsche Farbe an der Position 3/7 erkannt")

        if cube.pos4 in wuerfel_farben:
            cube.pos8 = nord_part.oben_links
        else:
            raise FalscheFarbeErkanntException("Falsche Farbe an der Position 4/8 erkannt")

        return cube
