import os
import sys

import cv2

from TurntableQuadrant import TurntableQuadrant

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "common"))


# TODO: Remove this temporary main
turntable = TurntableQuadrant("res/XGGR_XXRX.mp4")
turntable.frame_when_aligned(0, 90)
cv2.waitKey(0)

turntable.frame_when_aligned(46 + 80, 20)

cv2.waitKey(0)
turntable.frame_when_aligned(46 + 80 + 90, 20)

cv2.waitKey(0)
cv2.destroyAllWindows()
