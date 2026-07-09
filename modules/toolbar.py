import cv2

COLORS = {
    "RED": (0, 0, 255),
    "GREEN": (0, 255, 0),
    "BLUE": (255, 0, 0),
    "YELLOW": (0, 255, 255),
    "BLACK": (0, 0, 0),
    "ERASER": (0, 0, 0),
}

BUTTONS = [
    ("RED", 20),
    ("GREEN", 110),
    ("BLUE", 200),
    ("YELLOW", 290),
    ("BLACK", 380),
    ("ERASER", 470),
]

def draw_toolbar(frame):
    for name, x in BUTTONS:
        color = COLORS[name]
        cv2.rectangle(frame, (x, 10), (x + 70, 70), color, -1)
        cv2.rectangle(frame, (x, 10), (x + 70, 70), (255, 255, 255), 2)
        cv2.putText(frame, name[:3], (x + 8, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
    return frame

def get_selected_tool(x, y):
    if y > 70:
        return None

    for name, pos in BUTTONS:
        if pos <= x <= pos + 70:
            return name

    return None