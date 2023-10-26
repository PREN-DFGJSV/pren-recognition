# local dependencies
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "common"))

from Point import Point

import numpy as np

class Line:
    """A line is made from two connecting points.
    """

    __p1: Point
    __p2: Point

    def __init__(self, x1: int,  y1: int,  x2: int, y2: int):
        """Parameters:
        x1 (int): X-coordinate of point 1. 
        y1 (int): Y-coordinate of point 1. 
        x2 (int): X-coordinate of point 2. 
        y2 (int): Y-coordinate of point 2. 
        """

        self.__p1 = Point(x1, y1)
        self.__p2 = Point(x2, y2)

    @staticmethod
    def create_from_points(p1: Point, p2: Point) -> "Line":
        """Parameters:
        p1 Point(int, int): X and Y-coordinate of point 1. 
        p2 Point(int, int): X and Y-coordinate of point 2. 
        """

        return Line(p1.x, p1.y, p2.x, p2.y)
    
    def get_point1(self) -> Point:
        return Point(self.__p1.x, self.__p1.y)
    
    def get_point1_coordinates(self) -> (int, int):
        return self.__p1.get_tuple()
    
    def get_point2(self) -> Point:
        return Point(self.__p2.x, self.__p2.y)
    
    def get_point2_coordinates(self) -> (int, int):
        return self.__p2.get_tuple()
    
    def get_slope(self) -> float:
        return Line.calculate_slope(self.__p1, self.__p2)
    
    @staticmethod
    def calculate_slope(p1: Point, p2: Point) -> float:
        return (p2.y - p1.y) / (p2.x - p1.x)

    def get_length(self) -> float:
        return Line.calculate_length(self.__p1, self.__p2)
    
    @staticmethod
    def calculate_length(p1: Point, p2: Point) -> float:

        dx1 = p2.x - p1.x 
        dy1 = p2.y - p1.y

        return np.sqrt(dx1 * dx1 + dy1 * dy1)
    
    def get_angle(self) -> float:
        return Line.calculate_angle(self.__p1, self.__p2)
    
    def is_at_angle(self, angle_deg: float, deviation_threshold_deg: float = 0) -> bool:

        line_angle = self.get_angle()
        target_angle = angle_deg / 180 * np.pi
        threshold = deviation_threshold_deg / 180 * np.pi

        return line_angle >= target_angle - threshold and line_angle <= target_angle + threshold

    @staticmethod
    def calculate_angle(p1: Point, p2: Point, deviation_threshold_deg: float = 0) -> bool:

        dx = p2.x - p1.x 
        dy = p2.y - p1.y

        return np.abs(np.arctan2(dy, dx))

    def is_paralell_to(self, other_line: "Line") -> float:
        return Line.are_lines_paralell(self, other_line)
    
    @staticmethod
    def are_lines_paralell(line1: "Line", line2: "Line", deviation_threshold_deg: float = 0) -> bool:
        #https://stackoverflow.com/questions/23989355/checking-if-two-lines-are-nearly-parallel-gives-wrong-results

        dx1 = line1.__p2.x - line1.__p1.x 
        dy1 = line1.__p2.y - line1.__p1.y 
        dx2 = line2.__p2.x - line2.__p1.x 
        dy2 = line2.__p2.y - line2.__p1.y 

        cos_angle = np.abs((dx1 * dx2 + dy1 * dy2) / np.sqrt((dx1 * dx1 + dy1 * dy1) * (dx2 * dx2 + dy2 * dy2)))

        return cos_angle > 1 - deviation_threshold_deg / 180 * np.pi
    
    @staticmethod
    def calculate_line_intersection(line1: "Line", line2: "Line") -> Point:

        dx1 = line1.__p2.x - line1.__p1.x 
        dy1 = line1.__p2.y - line1.__p1.y 
        dx2 = line2.__p2.x - line2.__p1.x 
        dy2 = line2.__p2.y - line2.__p1.y
        
        denominator = dy2 * dx1 - dx2 * dy1
        if denominator == 0:
            raise Exception("Lines do not intersect")
                                                                                 
        a = line1.__p1.y - line2.__p1.y
        b = line1.__p1.x - line2.__p1.x

        numerator1 = dx2 * a - dy2 * b
        numerator2 = dx1 * a - dy1 * b

        a = numerator1 / denominator
        b = numerator2 / denominator
        
        return Point(
            line1.__p1.x + (a * dx1),
            line1.__p1.y + (a * dy1)
        )
