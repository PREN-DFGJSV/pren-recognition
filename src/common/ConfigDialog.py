import tkinter as tk
from src.common.ConfigProperties import ConfigProperties

config = ConfigProperties()

class ConfigDialog:
    __instance = None
    __root = None

    def __apply(self):
        config.ROI_UPPER_LEFT = (int(self.ROI_UPPER_LEFT_x_entry.get()), int(self.ROI_UPPER_LEFT_y_entry.get()))
        config.ROI_BOTTOM_RIGHT = (int(self.ROI_BOTTOM_RIGHT_x_entry.get()), int(self.ROI_BOTTOM_RIGHT_y_entry.get()))

        config.MESSPUNKT_OBEN_LINKS = (int(self.MESSPUNKT_OBEN_LINKS_x_entry.get()), int(self.MESSPUNKT_OBEN_LINKS_y_entry.get()))
        config.MESSPUNKT_OBEN_RECHTS = (int(self.MESSPUNKT_OBEN_RECHTS_x_entry.get()), int(self.MESSPUNKT_OBEN_RECHTS_y_entry.get()))
        config.MESSPUNKT_UNTEN_LINKS = (int(self.MESSPUNKT_UNTEN_LINKS_x_entry.get()), int(self.MESSPUNKT_UNTEN_LINKS_y_entry.get()))
        config.MESSPUNKT_UNTEN_RECHTS = (int(self.MESSPUNKT_UNTEN_RECHTS_x_entry.get()), int(self.MESSPUNKT_UNTEN_RECHTS_y_entry.get()))

    def __reset(self):
        config.reset()
        self.ROI_UPPER_LEFT_x_text.set(config.ROI_UPPER_LEFT[0])
        self.ROI_UPPER_LEFT_y_text.set(config.ROI_UPPER_LEFT[1])
        self.ROI_BOTTOM_RIGHT_x_text.set(config.ROI_BOTTOM_RIGHT[0])
        self.ROI_BOTTOM_RIGHT_y_text.set(config.ROI_BOTTOM_RIGHT[1])
        self.MESSPUNKT_OBEN_LINKS_x_text.set(config.MESSPUNKT_OBEN_LINKS[0])
        self.MESSPUNKT_OBEN_LINKS_y_text.set(config.MESSPUNKT_OBEN_LINKS[1])
        self.MESSPUNKT_OBEN_RECHTS_x_text.set(config.MESSPUNKT_OBEN_RECHTS[0])
        self.MESSPUNKT_OBEN_RECHTS_y_text.set(config.MESSPUNKT_OBEN_RECHTS[1])
        self.MESSPUNKT_UNTEN_LINKS_x_text.set(config.MESSPUNKT_UNTEN_LINKS[0])
        self.MESSPUNKT_UNTEN_LINKS_y_text.set(config.MESSPUNKT_UNTEN_LINKS[1])
        self.MESSPUNKT_UNTEN_RECHTS_x_text.set(config.MESSPUNKT_UNTEN_RECHTS[0])
        self.MESSPUNKT_UNTEN_RECHTS_y_text.set(config.MESSPUNKT_UNTEN_RECHTS[1])

    def show(self):
        self.__root.title("Würfelerkennung")
        self.__root.geometry("270x400")
        self.__root.update()

    def __new__(cls):
        if (cls.__instance is None):
            cls.__instance = super(ConfigDialog, cls).__new__(cls)
            if (not config.DEPLOY_ENV_PROD):
                cls.__instance.__root = tk.Tk()
                cls.__instance.__init()
    
        return cls.__instance
    
    def __init(self):
        # ROI
        self.ROI_UPPER_LEFT_label = tk.Label(self.__root, text="ROI_UPPER_LEFT", justify="left")
        self.ROI_UPPER_LEFT_label.place(x=0, y=0, width=130, height=25)
        self.ROI_UPPER_LEFT_x_text = tk.IntVar()
        self.ROI_UPPER_LEFT_x_text.set(config.ROI_UPPER_LEFT[0])
        self.ROI_UPPER_LEFT_x_entry = tk.Entry(self.__root, textvariable=self.ROI_UPPER_LEFT_x_text)
        self.ROI_UPPER_LEFT_x_entry.place(x=0, y=25, width=60, height=25)
        self.ROI_UPPER_LEFT_y_text = tk.IntVar()
        self.ROI_UPPER_LEFT_y_text.set(config.ROI_UPPER_LEFT[1])
        self.ROI_UPPER_LEFT_y_entry = tk.Entry(self.__root, textvariable=self.ROI_UPPER_LEFT_y_text)
        self.ROI_UPPER_LEFT_y_entry.place(x=70, y=25, width=60, height=25)

        self.ROI_BOTTOM_RIGHT_label = tk.Label(self.__root, text="ROI_BOTTOM_RIGHT", justify="left")
        self.ROI_BOTTOM_RIGHT_label.place(x=140, y=0, width=130, height=25)
        self.ROI_BOTTOM_RIGHT_x_text = tk.IntVar()
        self.ROI_BOTTOM_RIGHT_x_text.set(config.ROI_BOTTOM_RIGHT[0])
        self.ROI_BOTTOM_RIGHT_x_entry = tk.Entry(self.__root, textvariable=self.ROI_BOTTOM_RIGHT_x_text)
        self.ROI_BOTTOM_RIGHT_x_entry.place(x=140, y=25, width=60, height=25)
        self.ROI_BOTTOM_RIGHT_y_text = tk.IntVar()
        self.ROI_BOTTOM_RIGHT_y_text.set(config.ROI_BOTTOM_RIGHT[1])
        self.ROI_BOTTOM_RIGHT_y_entry = tk.Entry(self.__root, textvariable=self.ROI_BOTTOM_RIGHT_y_text)
        self.ROI_BOTTOM_RIGHT_y_entry.place(x=210, y=25, width=60, height=25)

        # Messpunkte
        self.MESSPUNKT_OBEN_LINKS_label = tk.Label(self.__root, text="MESSPUNKT_OBEN_LINKS", justify="left")
        self.MESSPUNKT_OBEN_LINKS_label.place(x=0, y=50, width=130, height=25)
        self.MESSPUNKT_OBEN_LINKS_x_text = tk.IntVar()
        self.MESSPUNKT_OBEN_LINKS_x_text.set(config.MESSPUNKT_OBEN_LINKS[0])
        self.MESSPUNKT_OBEN_LINKS_x_entry = tk.Entry(self.__root, textvariable=self.MESSPUNKT_OBEN_LINKS_x_text)
        self.MESSPUNKT_OBEN_LINKS_x_entry.place(x=0, y=75, width=60, height=25)
        self.MESSPUNKT_OBEN_LINKS_y_text = tk.IntVar()
        self.MESSPUNKT_OBEN_LINKS_y_text.set(config.MESSPUNKT_OBEN_LINKS[1])
        self.MESSPUNKT_OBEN_LINKS_y_entry = tk.Entry(self.__root, textvariable=self.MESSPUNKT_OBEN_LINKS_y_text)
        self.MESSPUNKT_OBEN_LINKS_y_entry.place(x=70, y=75, width=60, height=25)

        self.MESSPUNKT_OBEN_RECHTS_label = tk.Label(self.__root, text="MESSPUNKT_OBEN_RECHTS", justify="left")
        self.MESSPUNKT_OBEN_RECHTS_label.place(x=140, y=50, width=130, height=25)
        self.MESSPUNKT_OBEN_RECHTS_x_text = tk.IntVar()
        self.MESSPUNKT_OBEN_RECHTS_x_text.set(config.MESSPUNKT_OBEN_RECHTS[0])
        self.MESSPUNKT_OBEN_RECHTS_x_entry = tk.Entry(self.__root, textvariable=self.MESSPUNKT_OBEN_RECHTS_x_text)
        self.MESSPUNKT_OBEN_RECHTS_x_entry.place(x=140, y=75, width=60, height=25)
        self.MESSPUNKT_OBEN_RECHTS_y_text = tk.IntVar()
        self.MESSPUNKT_OBEN_RECHTS_y_text.set(config.MESSPUNKT_OBEN_RECHTS[1])
        self.MESSPUNKT_OBEN_RECHTS_y_entry = tk.Entry(self.__root, textvariable=self.MESSPUNKT_OBEN_RECHTS_y_text)
        self.MESSPUNKT_OBEN_RECHTS_y_entry.place(x=210, y=75, width=60, height=25)

        self.MESSPUNKT_UNTEN_LINKS_label = tk.Label(self.__root, text="MESSPUNKT_UNTEN_LINKS", justify="left")
        self.MESSPUNKT_UNTEN_LINKS_label.place(x=0, y=100, width=130, height=25)
        self.MESSPUNKT_UNTEN_LINKS_x_text = tk.IntVar()
        self.MESSPUNKT_UNTEN_LINKS_x_text.set(config.MESSPUNKT_UNTEN_LINKS[0])
        self.MESSPUNKT_UNTEN_LINKS_x_entry = tk.Entry(self.__root, textvariable=self.MESSPUNKT_UNTEN_LINKS_x_text)
        self.MESSPUNKT_UNTEN_LINKS_x_entry.place(x=0, y=125, width=60, height=25)
        self.MESSPUNKT_UNTEN_LINKS_y_text = tk.IntVar()
        self.MESSPUNKT_UNTEN_LINKS_y_text.set(config.MESSPUNKT_UNTEN_LINKS[1])
        self.MESSPUNKT_UNTEN_LINKS_y_entry = tk.Entry(self.__root, textvariable=self.MESSPUNKT_UNTEN_LINKS_y_text)
        self.MESSPUNKT_UNTEN_LINKS_y_entry.place(x=70, y=125, width=60, height=25)

        self.MESSPUNKT_UNTEN_RECHTS_label = tk.Label(self.__root, text="MESSPUNKT_UNTEN_RECHTS", justify="left")
        self.MESSPUNKT_UNTEN_RECHTS_label.place(x=140, y=100, width=130, height=25)
        self.MESSPUNKT_UNTEN_RECHTS_x_text = tk.IntVar()
        self.MESSPUNKT_UNTEN_RECHTS_x_text.set(config.MESSPUNKT_UNTEN_RECHTS[0])
        self.MESSPUNKT_UNTEN_RECHTS_x_entry = tk.Entry(self.__root, textvariable=self.MESSPUNKT_UNTEN_RECHTS_x_text)
        self.MESSPUNKT_UNTEN_RECHTS_x_entry.place(x=140, y=125, width=60, height=25)
        self.MESSPUNKT_UNTEN_RECHTS_y_text = tk.IntVar()
        self.MESSPUNKT_UNTEN_RECHTS_y_text.set(config.MESSPUNKT_UNTEN_RECHTS[1])
        self.MESSPUNKT_UNTEN_RECHTS_y_entry = tk.Entry(self.__root, textvariable=self.MESSPUNKT_UNTEN_RECHTS_y_text)
        self.MESSPUNKT_UNTEN_RECHTS_y_entry.place(x=210, y=125, width=60, height=25)

        # Controls
        self.apply_button = tk.Button(self.__root, text="Ändern", command=self.__apply)
        self.apply_button.place(x=0, y=250, width=130, height=25)

        self.reset_button = tk.Button(self.__root, text="Reset", command=self.__reset)
        self.reset_button.place(x=140, y=250, width=130, height=25)