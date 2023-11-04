from typing import Tuple

from src.enums.EOrientierung import EOrientierung
from src.model.CubePart import CubePart


class CubePartHelper:
    @staticmethod
    def change_cube_part_orientation(ost_part: CubePart, west_part: CubePart) -> Tuple[CubePart, CubePart]:
        new_nord_cube_part: CubePart = CubePart(
            orientierung=EOrientierung.NORD,
            unten_links=ost_part.unten_rechts,
            oben_links=ost_part.oben_rechts,
            unten_rechts=west_part.unten_links,
            oben_rechts=west_part.oben_rechts
        )
        new_sued_cube_part: CubePart = CubePart(
            orientierung=EOrientierung.SUED,
            unten_rechts=ost_part.unten_links,
            oben_rechts=ost_part.oben_links,
            unten_links=west_part.unten_rechts,
            oben_links=west_part.oben_rechts
        )

        return new_nord_cube_part, new_sued_cube_part
