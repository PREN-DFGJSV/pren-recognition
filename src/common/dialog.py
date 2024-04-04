import tkinter as tk
import src.config as config

if (not config.DEPLOY_ENV_PROD):
    root = tk.Tk()

def __apply():
    config.ROI_UPPER_LEFT = (int(ROI_UPPER_LEFT_x_entry.get()), int(ROI_UPPER_LEFT_y_entry.get()))
    config.ROI_BOTTOM_RIGHT = (int(ROI_BOTTOM_RIGHT_x_entry.get()), int(ROI_BOTTOM_RIGHT_y_entry.get()))

    config.MESSPUNKT_OBEN_LINKS = (int(MESSPUNKT_OBEN_LINKS_x_entry.get()), int(MESSPUNKT_OBEN_LINKS_y_entry.get()))
    config.MESSPUNKT_OBEN_RECHTS = (int(MESSPUNKT_OBEN_RECHTS_x_entry.get()), int(MESSPUNKT_OBEN_RECHTS_y_entry.get()))
    config.MESSPUNKT_UNTEN_LINKS = (int(MESSPUNKT_UNTEN_LINKS_x_entry.get()), int(MESSPUNKT_UNTEN_LINKS_y_entry.get()))
    config.MESSPUNKT_UNTEN_RECHTS = (int(MESSPUNKT_UNTEN_RECHTS_x_entry.get()), int(MESSPUNKT_UNTEN_RECHTS_y_entry.get()))

    print( config.ROI_UPPER_LEFT)

def __reset():
    ROI_UPPER_LEFT_x_text.set(config.ROI_UPPER_LEFT[0])

def showConfigDialog():
    root.title("Würfelerkennung")
    root.geometry("270x400")
    root.update()

# ROI
ROI_UPPER_LEFT_label = tk.Label(root, text="ROI_UPPER_LEFT", justify="left")
ROI_UPPER_LEFT_label.place(x=0, y=0, width=130, height=25)
ROI_UPPER_LEFT_x_text = tk.IntVar()
ROI_UPPER_LEFT_x_text.set(config.ROI_UPPER_LEFT[0])
ROI_UPPER_LEFT_x_entry = tk.Entry(root, textvariable=ROI_UPPER_LEFT_x_text)
ROI_UPPER_LEFT_x_entry.place(x=0, y=25, width=60, height=25)
ROI_UPPER_LEFT_y_text = tk.IntVar()
ROI_UPPER_LEFT_y_text.set(config.ROI_UPPER_LEFT[1])
ROI_UPPER_LEFT_y_entry = tk.Entry(root, textvariable=ROI_UPPER_LEFT_y_text)
ROI_UPPER_LEFT_y_entry.place(x=70, y=25, width=60, height=25)

ROI_BOTTOM_RIGHT_label = tk.Label(root, text="ROI_BOTTOM_RIGHT", justify="left")
ROI_BOTTOM_RIGHT_label.place(x=140, y=0, width=130, height=25)
ROI_BOTTOM_RIGHT_x_text = tk.IntVar()
ROI_BOTTOM_RIGHT_x_text.set(config.ROI_BOTTOM_RIGHT[0])
ROI_BOTTOM_RIGHT_x_entry = tk.Entry(root, textvariable=ROI_BOTTOM_RIGHT_x_text)
ROI_BOTTOM_RIGHT_x_entry.place(x=140, y=25, width=60, height=25)
ROI_BOTTOM_RIGHT_y_text = tk.IntVar()
ROI_BOTTOM_RIGHT_y_text.set(config.ROI_BOTTOM_RIGHT[1])
ROI_BOTTOM_RIGHT_y_entry = tk.Entry(root, textvariable=ROI_BOTTOM_RIGHT_y_text)
ROI_BOTTOM_RIGHT_y_entry.place(x=210, y=25, width=60, height=25)


# Messpunkte
MESSPUNKT_OBEN_LINKS_label = tk.Label(root, text="MESSPUNKT_OBEN_LINKS", justify="left")
MESSPUNKT_OBEN_LINKS_label.place(x=0, y=50, width=130, height=25)
MESSPUNKT_OBEN_LINKS_x_text = tk.IntVar()
MESSPUNKT_OBEN_LINKS_x_text.set(config.MESSPUNKT_OBEN_LINKS[0])
MESSPUNKT_OBEN_LINKS_x_entry = tk.Entry(root, textvariable=MESSPUNKT_OBEN_LINKS_x_text)
MESSPUNKT_OBEN_LINKS_x_entry.place(x=0, y=75, width=60, height=25)
MESSPUNKT_OBEN_LINKS_y_text = tk.IntVar()
MESSPUNKT_OBEN_LINKS_y_text.set(config.MESSPUNKT_OBEN_LINKS[1])
MESSPUNKT_OBEN_LINKS_y_entry = tk.Entry(root, textvariable=MESSPUNKT_OBEN_LINKS_y_text)
MESSPUNKT_OBEN_LINKS_y_entry.place(x=70, y=75, width=60, height=25)

MESSPUNKT_OBEN_RECHTS_label = tk.Label(root, text="MESSPUNKT_OBEN_RECHTS", justify="left")
MESSPUNKT_OBEN_RECHTS_label.place(x=140, y=50, width=130, height=25)
MESSPUNKT_OBEN_RECHTS_x_text = tk.IntVar()
MESSPUNKT_OBEN_RECHTS_x_text.set(config.MESSPUNKT_OBEN_RECHTS[0])
MESSPUNKT_OBEN_RECHTS_x_entry = tk.Entry(root, textvariable=MESSPUNKT_OBEN_RECHTS_x_text)
MESSPUNKT_OBEN_RECHTS_x_entry.place(x=140, y=75, width=60, height=25)
MESSPUNKT_OBEN_RECHTS_y_text = tk.IntVar()
MESSPUNKT_OBEN_RECHTS_y_text.set(config.MESSPUNKT_OBEN_RECHTS[1])
MESSPUNKT_OBEN_RECHTS_y_entry = tk.Entry(root, textvariable=MESSPUNKT_OBEN_RECHTS_y_text)
MESSPUNKT_OBEN_RECHTS_y_entry.place(x=210, y=75, width=60, height=25)

MESSPUNKT_UNTEN_LINKS_label = tk.Label(root, text="MESSPUNKT_UNTEN_LINKS", justify="left")
MESSPUNKT_UNTEN_LINKS_label.place(x=0, y=100, width=130, height=25)
MESSPUNKT_UNTEN_LINKS_x_text = tk.IntVar()
MESSPUNKT_UNTEN_LINKS_x_text.set(config.MESSPUNKT_UNTEN_LINKS[0])
MESSPUNKT_UNTEN_LINKS_x_entry = tk.Entry(root, textvariable=MESSPUNKT_UNTEN_LINKS_x_text)
MESSPUNKT_UNTEN_LINKS_x_entry.place(x=0, y=125, width=60, height=25)
MESSPUNKT_UNTEN_LINKS_y_text = tk.IntVar()
MESSPUNKT_UNTEN_LINKS_y_text.set(config.MESSPUNKT_UNTEN_LINKS[1])
MESSPUNKT_UNTEN_LINKS_y_entry = tk.Entry(root, textvariable=MESSPUNKT_UNTEN_LINKS_y_text)
MESSPUNKT_UNTEN_LINKS_y_entry.place(x=70, y=125, width=60, height=25)

MESSPUNKT_UNTEN_RECHTS_label = tk.Label(root, text="MESSPUNKT_UNTEN_RECHTS", justify="left")
MESSPUNKT_UNTEN_RECHTS_label.place(x=140, y=100, width=130, height=25)
MESSPUNKT_UNTEN_RECHTS_x_text = tk.IntVar()
MESSPUNKT_UNTEN_RECHTS_x_text.set(config.MESSPUNKT_UNTEN_RECHTS[0])
MESSPUNKT_UNTEN_RECHTS_x_entry = tk.Entry(root, textvariable=MESSPUNKT_UNTEN_RECHTS_x_text)
MESSPUNKT_UNTEN_RECHTS_x_entry.place(x=140, y=125, width=60, height=25)
MESSPUNKT_UNTEN_RECHTS_y_text = tk.IntVar()
MESSPUNKT_UNTEN_RECHTS_y_text.set(config.MESSPUNKT_UNTEN_RECHTS[1])
MESSPUNKT_UNTEN_RECHTS_y_entry = tk.Entry(root, textvariable=MESSPUNKT_UNTEN_RECHTS_y_text)
MESSPUNKT_UNTEN_RECHTS_y_entry.place(x=210, y=125, width=60, height=25)


# Controls
apply_button = tk.Button(root, text="Ändern", command=__apply)
apply_button.place(x=0, y=250, width=130, height=25)

reset_button = tk.Button(root, text="Reset", command=__reset)
reset_button.place(x=140, y=250, width=130, height=25)