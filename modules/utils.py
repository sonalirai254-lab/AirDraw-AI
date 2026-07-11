import cv2
import os
from datetime import datetime

def save_canvas(canvas):
    if not os.path.exists("saved"):
        os.makedirs("saved")

    filename = datetime.now().strftime("saved/drawing_%Y%m%d_%H%M%S.png")
    cv2.imwrite(filename, canvas)
    print("Saved:", filename)

def clear_canvas(canvas):
    canvas[:] = 0