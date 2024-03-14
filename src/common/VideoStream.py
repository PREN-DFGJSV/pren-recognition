import cv2

from src.common.constants import *

class VideoStream:
    
    @staticmethod
    def open_camera():
        cap = cv2.VideoCapture(
            "rtsp://" +
            RTSP_USERNAME + ":" + RTSP_PASSWORD +
            "@" + RTSP_URL +
            "?streamprofile=" + RTSP_PROFILE)
        
        if cap is None or not cap.isOpened():
            print("Video-Stream Error: Unable to open video source from ", RTSP_IP)
            return None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Video-Stream Error: Unable to read next frame")
                break
            
            cv2.imshow("Video-Stream (close with 'q')", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
