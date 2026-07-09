import cv2
import numpy as np


class DrawingCanvas:
    def __init__(self, width=640, height=480):
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.prev_x = 0
        self.prev_y = 0
        self.color = (0, 0, 255)
        self.thickness = 8
        self.undo_stack = []
        self.redo_stack = []

    def save_state(self):
        self.undo_stack.append(self.canvas.copy())
        self.redo_stack.clear()

    def draw(self, frame, x, y):
        if self.prev_x == 0 and self.prev_y == 0:
            self.save_state()
            self.prev_x = x
            self.prev_y = y

        cv2.line(self.canvas, (self.prev_x, self.prev_y), (x, y), self.color, self.thickness)
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
        self.save_state()
        self.canvas[:] = 0

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.canvas.copy())
            self.canvas = self.undo_stack.pop()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.canvas.copy())
            self.canvas = self.redo_stack.pop()