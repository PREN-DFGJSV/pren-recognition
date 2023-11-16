import cv2
import numpy as np

from typing import List

from src.enums.EOrientierung import EOrientierung
from src.common.ColorPair import ColorPair
from src.common.Video360 import Video360
from src.turntable_alignment.Line import Line
from src.turntable_alignment.AlignedFrame import AlignedFrame


# TODO: Add documentation for TurntableQuadrant
# TODO: Add functioanilty returning two frames with their orientation (N,E,S,W) and rotation center coordinates
class TurntableQuadrant:
    """Rotating turntable as specified in PREN. 
    Sectioned into four quadrants of which one is white and three are black. The rotation center may be obstructed by a construction of cubes.
    Default rotating speed is 2rpm ± 12° or ± 1s.
    """

    __video360: Video360

    def __init__(self, video_path: str, rpm: int = 2):
        """Parameters:
        video_path (str): Path and/or filename to video. 
        rpm (int): Turntable rotation speed given as rotations per minute. Default is 2.
        """

        self.__video360 = Video360(video_path, rpm)

    # TODO: How no detection should be handled?
    def detect_aligned_frames(self, start_angle: int = 0, max_angle_rotation: int = 95) -> List[AlignedFrame]:

        detected_frames: List[AlignedFrame] = []

        first_frame_found, first_frame_angle, first_frame = self.__retrieve_frame(start_angle, max_angle_rotation)

        if first_frame_found:
            detected_frames.append(first_frame)

            next_frame_found, next_frame_angle, next_frame = self.__retrieve_frame(first_frame_angle + 175, 10)

            if next_frame_found:
                detected_frames.append(next_frame)

        return detected_frames

    def __retrieve_frame(self, start_angle: int, max_angle_rotation: int) -> (bool, float, AlignedFrame):

        angle = start_angle
        quadrant_found = False

        while not quadrant_found and angle < start_angle + max_angle_rotation:
            aligned_frame_found, aligned_frame = self.__is_frame_aligned(angle)

            if aligned_frame_found:
                print(f"First aligned frame found at: {angle}° rotation!")
                return True, angle, aligned_frame

            # TODO: Optimize first frame detection, none static increment
            angle += 0.2

        print("No frame found!")
        return False, start_angle + max_angle_rotation, None

    def __is_frame_aligned(self, angle: float) -> (bool, AlignedFrame):
        img_original = self.__video360.frame_at_angle(angle)
        img_debug = img_original.copy()
        img_hsv = cv2.cvtColor(img_original, cv2.COLOR_BGR2HSV)

        mask_white = ColorPair.create_white_pair().get_mask(img_hsv)
        mask_white = cv2.GaussianBlur(mask_white, (1, 1), 0)
        image_quadrant_edges = cv2.Canny(mask_white, 100, 200)

        rho = 1  # distance resolution in pixels of the Hough grid
        theta = np.pi / 180  # angular resolution in radians of the Hough grid
        threshold = 50  # minimum number of votes (intersections in Hough grid cell)
        min_line_length = 100  # minimum number of pixels making up a line
        max_line_gap = 40  # maximum gap in pixels between connectable line segments

        hough_lines = cv2.HoughLinesP(image_quadrant_edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

        t_lines = []

        hor_line = 0
        vert_line = 0

        for line in hough_lines:
            for x1, y1, x2, y2 in line:
                t_lines.append(Line(x1, y1, x2, y2))
                color = np.random.randint(0, 255, size=(3,))
                color = (int(color[0]), int(color[1]), int(color[2]))

        t_lines.sort(key=lambda x: x.get_length(), reverse=True)

        for line in t_lines:
            if hor_line == 0 and (line.is_at_angle(0, 1) or line.is_at_angle(180, 1)):
                hor_line = line
            elif vert_line == 0 and (line.is_at_angle(90, 1) or line.is_at_angle(270, 1)):
                vert_line = line

        if hor_line != 0 and vert_line != 0:
            intersection_point = Line.calculate_line_intersection(hor_line, vert_line)
            x, y = intersection_point.get_tuple()

            cv2.line(img_debug, hor_line.get_point1_coordinates(), hor_line.get_point2_coordinates(), (255, 0, 0), 10)
            cv2.line(img_debug, vert_line.get_point1_coordinates(), vert_line.get_point2_coordinates(), (255, 0, 0), 10)
            cv2.circle(img_debug, (int(np.round(x)), int(np.round(y))), 4, (0, 255, 0), 5)

            return True, AlignedFrame(img_original, img_debug, intersection_point, EOrientierung.NORD)

        return False, None

    def mask_quadrants(self) -> None:
        img = self.__video360.frame_at_angle(0)
