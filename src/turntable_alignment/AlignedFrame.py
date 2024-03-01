from dataclasses import dataclass

import numpy as np

from src.enums.EOrientierung import EOrientierung
from src.turntable_alignment.Line import Line
from src.turntable_alignment.Point import Point

@dataclass
class AlignedFrame:
    """An aligned or found frame for further color recognition processing.
    It contains the image/frame itself, the calculated center point of the turntable
    and the orientation based on the location of the white colored turntable quadrant.
    """

    frame: np.ndarray
    debug_frame: np.ndarray # Found edge lines and center point are marked for debug purposes.
    frame_angle: float
    center: Point
    orientation: EOrientierung
    horizontal_line: Line
    vertical_line: Line

    def get(self) -> tuple[int, Point, EOrientierung]:
        return self.frame, self.center, self.orientation