import cv2
import numpy as np

from typing import List
from cv2.typing import MatLike

from src.common.Video360 import Video360
from src.common.constants import *
from src.enums.EOrientierung import EOrientierung
from src.common.ColorPair import ColorPair
from src.model.Line import Line
from src.model.AlignedFrame import AlignedFrame


# TODO: Add documentation for TurntableQuadrantStream
class TurntableQuadrantStream:
    """Rotating turntable as specified in PREN. 
    Sectioned into four quadrants of which one is white and three are black. The rotation center may be obstructed by a construction of cubes.
    """

    # TODO: How no detection should be handled?
    def detect_aligned_frames(self) -> List[AlignedFrame]:

        cap = cv2.VideoCapture(
            "rtsp://" +
            RTSP_USERNAME + ":" + RTSP_PASSWORD +
            "@" + RTSP_URL +
            "?streamprofile=" + RTSP_PROFILE)
         
        if cap is None or not cap.isOpened():
            print("Video-Stream: Error accessing stream", RTSP_IP)
            return None
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        current_frame_number = 0
        max_first_frame_number = Video360.frame_number_from_angle(TURNTABLE_RPM, fps, MAX_ANGLE_ROTATION_FIRST_FRAME)
        max_total_frame_number = Video360.frame_number_from_angle(TURNTABLE_RPM, fps, DETECT_FRAMES_COUNT * 90)

        print("Video-Stream: Analyzing stream with", fps, "fps")

        detected_frames: List[AlignedFrame] = []
        first_frame = None
        
        while first_frame is None and current_frame_number <= max_first_frame_number or current_frame_number <= max_total_frame_number:
            ret, frame = cap.read()
            if not ret:
                print("Video-Stream: Error reading next frame")
                break

            debug_stream = frame.copy()
            cv2.rectangle(debug_stream, ROI_UPPER_LEFT, ROI_BOTTOM_RIGHT, (100, 50, 200), 5)
            cv2.imshow("Video-Stream (close with 'q')", debug_stream)

            roi = frame[ROI_UPPER_LEFT[1] : ROI_BOTTOM_RIGHT[1], ROI_UPPER_LEFT[0] : ROI_BOTTOM_RIGHT[0]]

            if first_frame is None:

                first_frame = self.detect_aligned_frame(roi)

                if first_frame is not None:
                    first_frame.frame_angle = Video360.angle_from_frame_number(TURNTABLE_RPM, fps, current_frame_number)
                    detected_frames.append(first_frame)
                    print(f"First frame found after {round(current_frame_number / fps, 2)}s at {round(first_frame.frame_angle, 2)}° with {first_frame.orientation}!")
                    cv2.imshow(f"First frame ({round(current_frame_number / fps, 2)}s - {round(first_frame.frame_angle, 2)} deg - {first_frame.orientation})", first_frame.debug_frame)

            current_frame_number += 1

            # Abort
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            # TODO: Rem
            # Reset
            if cv2.waitKey(1) & 0xFF == ord("r"):
                print("Reset")
                first_frame = None
                current_frame_number = 0

        print(f"Table rotated maximum of {DETECT_FRAMES_COUNT * 90}°")

        return detected_frames   

    def detect_aligned_frame(self, frame) -> AlignedFrame:

        aligned_frame = self.__is_frame_aligned(frame)

        if aligned_frame is not None:
            aligned_frame = self.__set_orientation(aligned_frame)
            return aligned_frame

        return None
    
    def __is_frame_aligned(self, frame) -> AlignedFrame:

        frame, raw_lines = self.__detect_edge_lines_of_frame(frame)

        detected_lines_frame = frame.copy()
        debug_frame = frame.copy()

        if raw_lines is None:
            raw_lines = []

        lines = []

        for line in raw_lines:
            for x1, y1, x2, y2 in line:
                lines.append(Line(x1, y1, x2, y2))
                color = np.random.randint(0, 255, size=(3,))
                color = (int(color[0]), int(color[1]), int(color[2]))
                cv2.line(detected_lines_frame, (x1, y1), (x2, y2), color, 2)


        cv2.imshow("Quadrant HoughLines", detected_lines_frame)

        lines.sort(key=lambda x: x.get_length(), reverse=True)
        horizontal_line = None
        vertical_line = None

        for line in lines:
            if horizontal_line is None and (line.is_at_angle(0, ANGLE_DEVIATION_THRESHOLD_DEG) or line.is_at_angle(180, ANGLE_DEVIATION_THRESHOLD_DEG)):
                horizontal_line = line
            elif vertical_line is None and (line.is_at_angle(90, ANGLE_DEVIATION_THRESHOLD_DEG) or line.is_at_angle(270, ANGLE_DEVIATION_THRESHOLD_DEG)):
                vertical_line = line

        if horizontal_line is not None and vertical_line is not None:
            intersection_point = Line.calculate_line_intersection(horizontal_line, vertical_line)
            x, y = intersection_point.get_tuple()

            cv2.line(debug_frame, horizontal_line.get_point1_coordinates(), horizontal_line.get_point2_coordinates(), (255, 0, 0), 10)
            cv2.line(debug_frame, vertical_line.get_point1_coordinates(), vertical_line.get_point2_coordinates(), (255, 0, 0), 10)
            cv2.circle(debug_frame, (int(np.round(x)), int(np.round(y))), 4, (0, 255, 0), 5)

            return AlignedFrame(frame, debug_frame, 0, intersection_point, EOrientierung.NORD, horizontal_line, vertical_line)

        return None

    def __detect_edge_lines_of_frame(self, frame) -> tuple[np.ndarray, MatLike]:

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask_white = ColorPair(LOWER_WHITE, UPPER_WHITE).get_mask(frame_hsv)
        mask_white = cv2.GaussianBlur(mask_white, (1, 1), 0)

        quadrant_edges = cv2.Canny(mask_white, 100, 200)

        rho = 1  # distance resolution in pixels of the Hough grid
        theta = np.pi / 180  # angular resolution in radians of the Hough grid

        # TODO: Only show in debug mode
        cv2.imshow("White mask", mask_white)
        cv2.imshow("Quadrant edges", quadrant_edges)
        
        lines = cv2.HoughLinesP(quadrant_edges, rho, theta, LINE_THRESHOLD, np.array([]), LINE_MIN_PX_LENGTH, LINE_MAX_GAP)

        return (
            frame, 
            lines
        )
    
    def __set_orientation(self, aligned_frame: AlignedFrame) -> AlignedFrame:
            
            frame_hsv = cv2.cvtColor(aligned_frame.frame, cv2.COLOR_BGR2HSV)
            mask_white = ColorPair(LOWER_WHITE, UPPER_WHITE).get_mask(frame_hsv)
            mask_white = cv2.GaussianBlur(mask_white, (1, 1), 0)

            hor = round(aligned_frame.center.x)
            ver = round(aligned_frame.center.y)
            
            east_top_left_section = mask_white[:ver, :hor]
            north_top_right_section = mask_white[:ver, hor:]
            south_bottom_left_section = mask_white[ver:, :hor]
            west_bottom_right_section = mask_white[ver:, hor:]

            # total_white_px = np.sum(mask_white == 255) 
            # total_black_px = np.sum(mask_white == 0) 

            white_px = {
                'east_top_left_section_white_px': np.sum(east_top_left_section == 255),
                'north_top_right_section_white_px': np.sum(north_top_right_section == 255),
                'south_bottom_left_section_white_px': np.sum(south_bottom_left_section == 255),
                'west_bottom_right_section_white_px': np.sum(west_bottom_right_section == 255) 
            }

            orientation = EOrientierung.WEST

            match max(white_px, key=white_px.get):
                case 'east_top_left_section_white_px':
                    orientation = EOrientierung.OST
                case 'north_top_right_section_white_px':
                    orientation = EOrientierung.NORD
                case 'south_bottom_left_section_white_px':
                    orientation = EOrientierung.SUED

            aligned_frame.orientation = orientation
            return aligned_frame
