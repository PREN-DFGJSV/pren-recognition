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
            print("Video-Stream: Error accessing stream ", RTSP_IP)
            return None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Video-Stream: Error reading next frame")
                break

            cv2.rectangle(frame, ROI_UPPER_LEFT, ROI_BOTTOM_RIGHT, (100, 50, 200), 5)
            
            cv2.imshow("Video-Stream (close with 'q')", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
