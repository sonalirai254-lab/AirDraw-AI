import cv2
import os
import datetime
from modules.hand_tracker import HandTracker
from modules.toolbar import draw_toolbar, get_selected_tool, COLORS
from modules.drawing import DrawingCanvas


def save_drawing(canvas):
    os.makedirs("drawings", exist_ok=True)
    filename = datetime.datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
    path = os.path.join("drawings", filename)
    cv2.imwrite(path, canvas)
    return path


def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    drawing = DrawingCanvas()
    current_tool = "RED"

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        frame, landmarks = tracker.find_hand(frame)
        frame = draw_toolbar(frame)

        if landmarks:
            x, y = landmarks[8][1], landmarks[8][2]
            selected_tool = get_selected_tool(x, y)

            if selected_tool:
                current_tool = selected_tool
                drawing.reset_previous()

                if selected_tool == "ERASER":
                    drawing.change_color((0, 0, 0))
                    drawing.change_brush_size(35)
                else:
                    drawing.change_color(COLORS[selected_tool])
                    drawing.change_brush_size(8)
            else:
                if y > 80:
                    frame = drawing.draw(frame, x, y)

            cv2.circle(frame, (x, y), 10, (0, 0, 255), cv2.FILLED)
        else:
            drawing.reset_previous()

        cv2.putText(
            frame,
            f"Tool: {current_tool} | C Clear | S Save | U Undo | R Redo | Q Quit",
            (20, 470),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        cv2.imshow("AirDraw AI", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        elif key == ord("c"):
            drawing.clear()
        elif key == ord("s"):
            save_drawing(drawing.canvas)
        elif key == ord("u"):
            drawing.undo()
        elif key == ord("r"):
            drawing.redo()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()