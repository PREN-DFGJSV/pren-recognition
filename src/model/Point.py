from dataclasses import dataclass

@dataclass
class Point:
    """Represents a point in a 2D space.
    Multiple points can be connected to form a line.
    """

    x: int
    y: int

    def get_tuple(self) -> tuple[int, int]:
        return self.x, self.y
    