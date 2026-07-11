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

    def draw_on_canvas(self, x, y):
        if self.prev_x == 0 and self.prev_y == 0:
            self.save_state()
            self.prev_x, self.prev_y = x, y

        cv2.line(
            self.canvas,
            (self.prev_x, self.prev_y),
            (x, y),
            self.color,
            self.thickness
        )

        self.prev_x, self.prev_y = x, y

    def show_canvas(self, frame):
        return cv2.add(frame, self.canvas)

    def draw(self, frame, x, y):
        self.draw_on_canvas(x, y)
        return self.show_canvas(frame)

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
        self.reset_previous()

    def draw_circle(self):
        self.save_state()
        cv2.circle(
            self.canvas,
            (320, 240),
            80,
            self.color,
            self.thickness
        )

    def draw_rectangle(self):
        self.save_state()
        cv2.rectangle(
            self.canvas,
            (220, 160),
            (420, 320),
            self.color,
            self.thickness
        )

    def draw_line(self):
        self.save_state()
        cv2.line(
            self.canvas,
            (180, 240),
            (460, 240),
            self.color,
            self.thickness
        )

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.canvas.copy())
            self.canvas = self.undo_stack.pop()
            self.reset_previous()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.canvas.copy())
            self.canvas = self.redo_stack.pop()
            self.reset_previous()