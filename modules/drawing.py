import cv2
import numpy as np

class DrawingCanvas:
    def __init__(self, width=640, height=480):
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.prev_x = 0
        self.prev_y = 0
        self.color = (255, 0, 255)
        self.thickness = 8

    def draw(self, frame, x, y):
        if self.prev_x == 0 and self.prev_y == 0:
            self.prev_x, self.prev_y = x, y

        cv2.line(self.canvas, (self.prev_x, self.prev_y), (x, y), self.color, self.thickness)
        self.prev_x, self.prev_y = x, y

        frame = cv2.add(frame, self.canvas)
        return frame

    def reset_previous(self):
        self.prev_x = 0
        self.prev_y = 0

    def clear(self):
        self.canvas[:] = 0