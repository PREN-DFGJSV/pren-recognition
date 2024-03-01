import cv2
import numpy as np

from typing import List
from cv2.typing import MatLike

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

        first_frame = self.__retrieve_frame(start_angle, max_angle_rotation)

        if first_frame is not None:
            detected_frames.append(first_frame)

            next_frame = self.__retrieve_frame(first_frame.frame_angle + 175, 10)

            if next_frame is not None:
                detected_frames.append(next_frame)

        return detected_frames

    def __retrieve_frame(self, start_angle: int, max_angle_rotation: int) -> AlignedFrame:

        brute_step_increment_deg = 5
        fine_step_increment_deg = 0.1

        angle = start_angle
        quadrant_found = False

        while not quadrant_found and angle < start_angle + max_angle_rotation:
            aligned_frame = self.__is_frame_aligned(angle, 5)

            if aligned_frame is not None:
                print(f"Aligned frame roughly at {angle}°!")

                fine_angle: float = angle - brute_step_increment_deg
                aligned_frames: List[AlignedFrame] = []

                while fine_angle < angle + brute_step_increment_deg:   
                    aligned_fine_frame = self.__is_frame_aligned(fine_angle, 1)
                    if aligned_fine_frame is not None:
                        aligned_frames.append(aligned_fine_frame)
                    fine_angle += fine_step_increment_deg

                if aligned_frames:
                    aligned_frames.sort(key=lambda x: x.vertical_line.deviation_from_vertical_deg(), reverse=True)
                    print(f"Aligned frame exactly at {aligned_frames[0].frame_angle}°!")
                    return aligned_frames[0]
                
                return aligned_frame

            angle += brute_step_increment_deg

        print("No frame found!")
        return None
    
    def __is_frame_aligned(self, angle: float, angle_deviation_threshold_deg: float = 2) -> AlignedFrame:

        frame, raw_lines = self.__detect_edge_lines_of_frame(angle)
        debug_frame = frame.copy()

        lines = []

        for line in raw_lines:
            for x1, y1, x2, y2 in line:
                lines.append(Line(x1, y1, x2, y2))
                color = np.random.randint(0, 255, size=(3,))
                color = (int(color[0]), int(color[1]), int(color[2]))

        lines.sort(key=lambda x: x.get_length(), reverse=True)
        horizontal_line = None
        vertical_line = None

        for line in lines:
            if horizontal_line is None and (line.is_at_angle(0, angle_deviation_threshold_deg) or line.is_at_angle(180, angle_deviation_threshold_deg)):
                horizontal_line = line
            elif vertical_line is None and (line.is_at_angle(90, angle_deviation_threshold_deg) or line.is_at_angle(270, angle_deviation_threshold_deg)):
                vertical_line = line

        if horizontal_line is not None and vertical_line is not None:
            intersection_point = Line.calculate_line_intersection(horizontal_line, vertical_line)
            x, y = intersection_point.get_tuple()

            cv2.line(debug_frame, horizontal_line.get_point1_coordinates(), horizontal_line.get_point2_coordinates(), (255, 0, 0), 10)
            cv2.line(debug_frame, vertical_line.get_point1_coordinates(), vertical_line.get_point2_coordinates(), (255, 0, 0), 10)
            cv2.circle(debug_frame, (int(np.round(x)), int(np.round(y))), 4, (0, 255, 0), 5)

            return self.__get_aligned_frame(frame, debug_frame, angle, intersection_point, horizontal_line, vertical_line)

        return None

    def __detect_edge_lines_of_frame(self, angle: float) -> tuple[np.ndarray, MatLike]:
        frame = self.__video360.frame_at_angle(angle)
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask_white = ColorPair.create_white_pair().get_mask(frame_hsv)
        mask_white = cv2.GaussianBlur(mask_white, (1, 1), 0)
        quadrant_edges = cv2.Canny(mask_white, 100, 200)

        rho = 1  # distance resolution in pixels of the Hough grid
        theta = np.pi / 180  # angular resolution in radians of the Hough grid
        threshold = 50  # minimum number of votes (intersections in Hough grid cell)
        min_line_length = 100  # minimum number of pixels making up a line
        max_line_gap = 40  # maximum gap in pixels between connectable line segments

        return (
            frame, 
            cv2.HoughLinesP(quadrant_edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
        )
    
    def __get_aligned_frame(self, frame, debug_frame, angle, intersection_point, horizontal_line, vertical_line) -> AlignedFrame:
            
            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask_white = ColorPair.create_white_pair().get_mask(frame_hsv)
            mask_white = cv2.GaussianBlur(mask_white, (1, 1), 0)

            orientation = EOrientierung.NORD
            
            # TODO: Implement orientation detection

            return AlignedFrame(frame, debug_frame, angle, intersection_point, orientation, horizontal_line, vertical_line)
