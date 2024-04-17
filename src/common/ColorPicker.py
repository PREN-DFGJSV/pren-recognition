import cv2
import numpy as np

image_hsv = cv2.imread("res/color_picker/pick.png")
pixel = (0, 0, 0)

def pick_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y, x]

        lower =  np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
        upper =  np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        print(pixel, lower, upper)