from datetime import datetime

import cv2

from src.communication import WebServer
from src.common.ConfigProperties import ConfigProperties
from src.services.RecognitionService import RecognitionService
from src.common.ColorPicker import pick_color
from src.services.ValidationService import ValidationService

config = ConfigProperties()


if __name__ == "__main__":

    print(f"[{'PROD' if config.DEPLOY_ENV_PROD else 'DEV'}] Start Programm...", flush=True)

    if (config.DEPLOY_ENV_PROD):
        WebServer.app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        if (config.DEBUG_SHOW_COLOR_PICKER):
            cv2.namedWindow("Color_Picker")
            cv2.setMouseCallback("Color_Picker", pick_color)
            image_hsv = cv2.cvtColor(cv2.imread("res/color_picker/pick.png"), cv2.COLOR_BGR2HSV)
            cv2.imshow("Color_Picker", image_hsv)

        start_time = datetime.now()
        ValidationService.send_start_to_validation_server()
        RecognitionService.analyze_turntable_video_stream()
        end_time = datetime.now()
        ValidationService.send_to_validation_server(end_time-start_time)
        ValidationService.send_end_to_validation_server()
        # RecognitionService.test_fill_with_static_data()
        # RecognitionService.test_reading_instructions()

    print("End Programm...", flush=True)
