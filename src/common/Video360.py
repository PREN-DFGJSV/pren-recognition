import cv2
import numpy as np


class Video360:
    """A 360° video sequence taken from a 360° rotating camera or from a static camera capturing a turntable."""

    __video: cv2.VideoCapture
    __video_fps: int
    __video_frames_count: int
    __rpm: int

    def __init__(self, video_path: str, rpm: int):
        """Parameters:
        video_path (str): Path and/or filename to video. 
        rpm (int): Turntable rotation speed given as rotations per minute.
        """

        self.__video = cv2.VideoCapture(video_path)
        self.__video_fps = self.__video.get(cv2.CAP_PROP_FPS)
        self.__video_frames_count = self.__video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.__rpm = rpm

    def frame_at_angle(self, deg: float) -> np.ndarray:
        """Extracts frame/image from video at certain angle.

        Parameters:
        deg (float): Delta angle given in degrees.

        Returns:
        numpy.ndarray: Frame/image extracted from video using calculated frame number.
        """

        frame_number: int = Video360.frame_number_from_angle(self.__rpm, self.__video_fps, deg)

        if frame_number < 0 or frame_number > self.__video_frames_count:
            raise Exception("IllegalArgumentException: Deegrees/frame out of bound!")
        
        self.__video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        res, frame = self.__video.read()

        return frame

    @staticmethod
    def frame_number_from_angle(rpm: int, fps: int, deg: float) -> int:
        """Calculates frame(-number) of rotation from a given delta angle in degrees and turntable rpm. TIME = DEG / DPS. FRAME = TIME * FPS.

        Parameters:
        rpm (int): Turntable rotation speed given as rotations per minute.
        fps (int): Frames per second of given video feed.
        deg (float): Delta angle given in degrees.

        Returns:
        int: Frame(-number) or index specifying when delta angle is reached in video.
        """

        dps: int = Video360.convert_rpm_to_dps(rpm)
        time_seconds: float = deg / dps

        return round(time_seconds * fps)
    
    @staticmethod
    def angle_from_frame_number(rpm: int, fps: int, frame_number: int) -> float:
        """Calculates frame(-number) of rotation from a given delta angle in degrees and turntable rpm. TIME = DEG / DPS. FRAME = TIME * FPS.

        Parameters:
        rpm (int): Turntable rotation speed given as rotations per minute.
        fps (int): Frames per second of given video feed.
        frame_number (int): Frame(-number) or index specifying when delta angle is reached in video.

        Returns:
        float: Delta angle given in degrees.
        """

        dps: int = Video360.convert_rpm_to_dps(rpm)
        time_passed_seconds: float = frame_number / fps

        return time_passed_seconds * dps
    
    @staticmethod
    def convert_rpm_to_dps(rpm: int) -> int:
        """Converts RPM (rotations per minute) to DPS (degrees per second). DPS = RPM * 360° / 60s = RPM * 6°s.

        Parameters:
        rpm (int): Turntable rotation speed given as rotations per minute.

        Returns:
        int: Turntable rotation speed given as degrees per second.
        """

        return rpm * 6
