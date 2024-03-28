import tkinter as tk
import src.config as config

root = tk.Tk()

def __apply():
    config.ROI_UPPER_LEFT = (int(ROI_UPPER_LEFT_x_entry.get()), int(ROI_UPPER_LEFT_y_entry.get()))
    config.ROI_BOTTOM_RIGHT = (int(ROI_BOTTOM_RIGHT_x_entry.get()), int(ROI_BOTTOM_RIGHT_y_entry.get()))

    print( config.ROI_UPPER_LEFT)

def __reset():
    ROI_UPPER_LEFT_x_text.set(config.ROI_UPPER_LEFT[0])

def showConfigDialog():
    root.title("Würfelerkennung")
    root.geometry("270x400")
    root.update()

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

apply_button = tk.Button(root, text="Ändern", command=__apply)
apply_button.place(x=0, y=55, width=130, height=25)

reset_button = tk.Button(root, text="Reset", command=__reset)
reset_button.place(x=140, y=55, width=130, height=25)