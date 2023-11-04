from dataclasses import dataclass


# TODO: Add documentation for Point
@dataclass
class Point:
    x: int
    y: int

    def get_tuple(self) -> (int, int):
        return self.x, self.y
    