from dataclasses import dataclass

import numpy as np

from src.enums.EOrientierung import EOrientierung
from src.turntable_alignment.Point import Point

# TODO: Add documentation for found frame
@dataclass
class AlignedFrame:
    original_frame: np.ndarray
    debug_frame: np.ndarray
    center: Point
    orientation: EOrientierung

    def get(self) -> (int, Point, EOrientierung):
        return self.frame, self.center, self.orientation