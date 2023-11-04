import os
import sys

import cv2
import numpy as np

from Line import Line
from src.common.ColorPair import ColorPair
from src.common.Video360 import Video360

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "common"))


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

    def frame_when_aligned(self, start_deg=0, limit_rotation_deg=90):

        angle = start_deg
        quadrant_found = False

        while not quadrant_found and angle < start_deg + limit_rotation_deg:
            is_frame_aligned, frame = self.__retrieve_single_frame(angle)

            if is_frame_aligned:
                print("Frame aligned at: ", angle, "° rotation")
                cv2.imshow("Lines", frame)
                return

            angle += 0.2

        print("No frame found")

    def __retrieve_single_frame(self, angle: float):

        img_original = self.__video360.frame_at_angle(angle)
        img_hsv = cv2.cvtColor(img_original, cv2.COLOR_BGR2HSV)

        mask_white = ColorPair.create_white_pair().get_mask(img_hsv)
        mask_white = cv2.GaussianBlur(mask_white, (1, 1), 0)
        image_quadrant_edges = cv2.Canny(mask_white, 100, 200)

        rho = 1  # distance resolution in pixels of the Hough grid
        theta = np.pi / 180  # angular resolution in radians of the Hough grid
        threshold = 50  # minimum number of votes (intersections in Hough grid cell)
        min_line_length = 100  # minimum number of pixels making up a line
        max_line_gap = 40  # maximum gap in pixels between connectable line segments

        hough_lines = cv2.HoughLinesP(image_quadrant_edges, rho, theta, threshold, np.array([]), min_line_length,
                                      max_line_gap)

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
            intersection = Line.calculate_line_intersection(hor_line, vert_line)
            x, y = intersection.get_tuple()

            cv2.line(img_original, hor_line.get_point1_coordinates(), hor_line.get_point2_coordinates(), (255, 0, 0),
                     10)
            cv2.line(img_original, vert_line.get_point1_coordinates(), vert_line.get_point2_coordinates(), (255, 0, 0),
                     10)
            cv2.circle(img_original, (int(np.round(x)), int(np.round(y))), 4, (0, 255, 0), 5)

            return True, img_original

        return False, 0

    def mask_quadrants(self) -> None:
        img = self.__video360.frame_at_angle(0)
