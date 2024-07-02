"""This file defines project-level constants."""
import os
import numpy as np

class ConfigProperties:
    __instance = None

    # Environment
    DEPLOY_ENV = os.getenv("DEPLOY_ENV")
    DEPLOY_ENV_PROD = True if DEPLOY_ENV == "prod" else False
    DEPLOY_PORT = os.getenv("PORT")

    # Farberkennung
    MESSPUNKT_OBEN_LINKS = (190, 10)
    MESSPUNKT_OBEN_RECHTS = (250, 10)
    MESSPUNKT_UNTEN_LINKS = (190, 150)
    MESSPUNKT_UNTEN_RECHTS = (250, 150)
    SEITENLAENGE_MESSFLAECHE = 15

    # Rotationszentrum
    ROTATIONSPUNKT = (225, 145)
    USE_STATIC_ROTATIONSPUNKT = True

    # Camera/Frame Region of Interest
    ROI_UPPER_LEFT = (100, 50)
    ROI_BOTTOM_RIGHT = (550, 350)

    # Farbbereiche
    LOWER_RED = np.array([30, 25, 104])
    UPPER_RED = np.array([68, 63, 288])

    LOWER_YELLOW = np.array([3, 142, 116])
    UPPER_YELLOW = np.array([23, 162, 196])

    LOWER_BLUE = np.array([132, 58, -15])
    UPPER_BLUE = np.array([258, 119, 50])

    LOWER_WHITE = np.array([0, 0, 168])
    UPPER_WHITE = np.array([172, 111, 255])

    LOWER_BLACK = np.array([0, 0, 0])
    UPPER_BLACK = np.array([180, 255, 40])

    # Ausrichtung Linienerkennung
    LINE_THRESHOLD = 50                     # minimum number of votes (intersections in Hough grid cell)
    LINE_MIN_PX_LENGTH = 100                # minimum number of pixels making up a line
    LINE_MAX_GAP = 40                       # maximum gap in pixels between connectable line segments

    ANGLE_DEVIATION_THRESHOLD_DEG = 4       # How much the vertical or horizontal line is allowed to deviate. (±)
    DETECT_FRAMES_COUNT: int = 4            # Maximal count of aligned frames to be detected and returned.
    DETECT_FRAMES_STEP: int = 90
    MAX_ANGLE_ROTATION_FIRST_FRAME = 275
    TURNTABLE_RPM = 2.3                     # Turntable rotation speed given as rotations per minute. Specified in PREN is 2rpm (12°/s). -> Real RPM deviates!

    # API & RTSP Konfiguration
    RTSP_IP = "147.88.48.131:554" if DEPLOY_ENV_PROD else "147.88.48.131:554"
    RTSP_PATH = "/axis-media/media.amp"
    RTSP_URL = RTSP_IP + RTSP_PATH
    RTSP_USERNAME = "pren"
    RTSP_PASSWORD = "463997"
    RTSP_PROFILE = "pren_profile_med"     # "pren_profile_small" or "pren_profile_med"

    # Validierungsschnittstelle
    # DEV: https://ubqs3u6r81.execute-api.eu-central-1.amazonaws.com
    # PROD: https://oawz3wjih1.execute-api.eu-central-1.amazonaws.com
    VALIDATION_URL = "https://oawz3wjih1.execute-api.eu-central-1.amazonaws.com"
    VALIDATION_TEAM_ID = "team06"
    VALIDATION_TOKEN = "t7s9EUv3nOwk"

    # Database
    DATABASE_NAME = "results.db"

    # Ausrichtung Linienerkennung
    DEBUG_SHOW_LIVESTREAM = True
    DEBUG_SHOW_WHITE_MASK = False
    DEBUG_SHOW_CONTOUR = False
    DEBUG_SHOW_HOUGH_LINES = True
    DEBUG_SHOW_DETECTED_FRAME = True
    DEBUG_SHOW_COLOR_PICKER = False
    DEBUG_SHOW_COLOR_MASK = False

    def __new__(cls):
        if (cls.__instance is None):
            cls.__instance = super(ConfigProperties, cls).__new__(cls)
            cls.__instance.reset()
    
        return cls.__instance
    
    def reset(self):
        self.DEPLOY_ENV = os.getenv("DEPLOY_ENV")
        self.DEPLOY_ENV_PROD = True if self.DEPLOY_ENV == "prod" else False
        self.DEPLOY_PORT = os.getenv("PORT")
        
        self.MESSPUNKT_OBEN_LINKS = self.loadEnvConfigPoint("MESSPUNKT_OBEN_LINKS", 190, 30)
        self.MESSPUNKT_OBEN_RECHTS = self.loadEnvConfigPoint("MESSPUNKT_OBEN_RECHTS", 250, 30)
        self.MESSPUNKT_UNTEN_LINKS = self.loadEnvConfigPoint("MESSPUNKT_UNTEN_LINKS", 190, 170)
        self.MESSPUNKT_UNTEN_RECHTS = self.loadEnvConfigPoint("MESSPUNKT_UNTEN_RECHTS", 250, 170)
        self.ROTATIONSPUNKT = self.loadEnvConfigPoint("ROTATIONSPUNKT", 225, 145)
        self.USE_STATIC_ROTATIONSPUNKT = self.loadEnvConfigBool("USE_STATIC_ROTATIONSPUNKT", True)
        self.SEITENLAENGE_MESSFLAECHE = 15
        self.ROI_UPPER_LEFT = self.loadEnvConfigPoint("ROI_UPPER_LEFT", 80, 30)
        self.ROI_BOTTOM_RIGHT = self.loadEnvConfigPoint("ROI_BOTTOM_RIGHT", 550, 370)
        self.LOWER_RED = np.array([30, 25, 104])
        self.UPPER_RED = np.array([68, 63, 288])
        self.LOWER_YELLOW = np.array([60, 175, 183])
        self.UPPER_YELLOW = np.array([23, 213, 220])
        self.LOWER_BLUE = np.array([108, 47, -13])
        self.UPPER_BLUE = np.array([258, 119, 50])
        self.LOWER_WHITE = np.array([0, 0, 168])
        self.UPPER_WHITE = np.array([172, 111, 255])
        self.LOWER_BLACK = np.array([0, 0, 0])
        self.UPPER_BLACK = np.array([180, 255, 40])
        self.LINE_THRESHOLD = 50 
        self.LINE_MIN_PX_LENGTH = 100 
        self.LINE_MAX_GAP = 30 
        self.ANGLE_DEVIATION_THRESHOLD_DEG = 2 
        self.DETECT_FRAMES_COUNT: int = 3
        self.DETECT_FRAMES_STEP: int = 90
        self.MAX_ANGLE_ROTATION_FIRST_FRAME = 275
        self.TURNTABLE_RPM = 2.3
        self.RTSP_IP = "147.88.48.131:554" if self.DEPLOY_ENV_PROD else "147.88.48.131:554"
        self.RTSP_PATH = "/axis-media/media.amp"
        self.RTSP_URL = self.RTSP_IP + self.RTSP_PATH
        self.RTSP_USERNAME = "pren"
        self.RTSP_PASSWORD = "463997"
        self.RTSP_PROFILE = "pren_profile_small"
        self.DEBUG_SHOW_LIVESTREAM = True
        self.DEBUG_SHOW_WHITE_MASK = False
        self.DEBUG_SHOW_CONTOUR = False
        self.DEBUG_SHOW_HOUGH_LINES = True
        self.DEBUG_SHOW_DETECTED_FRAME = True
        self.DEBUG_SHOW_COLOR_PICKER = False
        self.DEBUG_SHOW_COLOR_MASK = False
        self.VALIDATION_URL = self.loadEnvConfig("VALIDATION_URL", "https://oawz3wjih1.execute-api.eu-central-1.amazonaws.com")
        self.VALIDATION_TEAM_ID = self.loadEnvConfig("VALIDATION_TEAM_ID", "team06")
        self.VALIDATION_TOKEN = self.loadEnvConfig("VALIDATION_TOKEN", "t7s9EUv3nOwk")

    def loadEnvConfig(self, env_name: str, default_val: str) -> str:
        if self.DEPLOY_ENV_PROD and os.getenv(env_name) is not None:
            val = os.getenv(env_name, default = default_val)
            print(f"Loaded env config for '{env_name}' with value '{val}' (default='{default_val}')", flush = True)
            return val
        return default_val
    
    def loadEnvConfigPoint(self, env_name: str, default_x: int, default_y: int) -> tuple[int, int]:
        if self.DEPLOY_ENV_PROD:
            val_x = self.loadEnvConfigInt(f'{env_name}_X', default_x)
            val_y = self.loadEnvConfigInt(f'{env_name}_Y', default_y)
            return (val_x, val_y)
        
        return (default_x, default_y)
    
    def loadEnvConfigInt(self, env_name: str, default_val: int) -> int:
        if self.DEPLOY_ENV_PROD and os.getenv(env_name) is not None:
            val = os.getenv(env_name, default = default_val)
            print(f"Loaded env config for '{env_name}' with value '{val}' (default='{default_val}')", flush = True)
            return val
        return default_val
    
    def loadEnvConfigBool(self, env_name: str, default_val: bool) -> bool:
        if self.DEPLOY_ENV_PROD and os.getenv(env_name) is not None:
            val = True if os.getenv(env_name, default = str(default_val)) == "True" else False
            print(f"Loaded env config for '{env_name}' with value {val} (default={default_val})", flush = True)
            return val
        return default_val