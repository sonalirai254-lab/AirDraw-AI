import cv2
import numpy as np


class DrawingCanvas:
    def __init__(self, width=640, height=480):
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)

        self.prev_x = 0
        self.prev_y = 0

        self.color = (0, 0, 255)  # Default Red
        self.thickness = 8

    def draw(self, frame, x, y):

        if self.prev_x == 0 and self.prev_y == 0:
            self.prev_x = x
            self.prev_y = y

        cv2.line(
            self.canvas,
            (self.prev_x, self.prev_y),
            (x, y),
            self.color,
            self.thickness,
        )

        self.prev_x = x
        self.prev_y = y

        return cv2.add(frame, self.canvas)

    def change_color(self, color):
        self.color = color

    def change_brush_size(self, size):
        self.thickness = size

    def reset_previous(self):
        self.prev_x = 0
        self.prev_y = 0

    def clear(self):
        self.canvas[:] = 0