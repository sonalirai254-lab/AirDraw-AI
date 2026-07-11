import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import cv2
import datetime

from modules.hand_tracker import HandTracker
from modules.toolbar import draw_toolbar, get_selected_tool, COLORS
from modules.drawing import DrawingCanvas
from modules.gestures import GestureDetector
from modules.shape_detector import detect_shape


def save_drawing(canvas):
    os.makedirs("drawings", exist_ok=True)

    filename = datetime.datetime.now().strftime(
        "drawing_%Y%m%d_%H%M%S.png"
    )

    path = os.path.join("drawings", filename)

    cv2.imwrite(path, canvas)

    print("Drawing saved:", path)

    return path


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera not found.")
        return

    tracker = HandTracker()
    drawing = DrawingCanvas()
    gesture_detector = GestureDetector()

    current_tool = "RED"
    clear_done = False
    detected_shape = "None"

    while True:
        success, frame = cap.read()

        if not success:
            print("Could not read camera frame.")
            break

        frame = cv2.flip(frame, 1)

        frame, landmarks = tracker.find_hand(frame)

        gesture = gesture_detector.detect(landmarks)

        if landmarks:
            x = landmarks[8][1]
            y = landmarks[8][2]

            if gesture == "CLEAR":
                if not clear_done:
                    drawing.clear()
                    clear_done = True

                drawing.reset_previous()

            elif gesture == "SELECT":
                selected_tool = get_selected_tool(x, y)

                if selected_tool:
                    current_tool = selected_tool
                    drawing.reset_previous()

                    if selected_tool == "ERASER":
                        drawing.change_color((0, 0, 0))
                        drawing.change_brush_size(35)

                    elif selected_tool == "SMALL":
                        drawing.change_brush_size(4)

                    elif selected_tool == "MEDIUM":
                        drawing.change_brush_size(8)

                    elif selected_tool == "LARGE":
                        drawing.change_brush_size(16)

                    else:
                        drawing.change_color(COLORS[selected_tool])

                clear_done = False

            elif gesture == "DRAW":
                clear_done = False

                if y > 80:
                    drawing.draw_on_canvas(x, y)

            else:
                drawing.reset_previous()
                clear_done = False

            cv2.circle(
                frame,
                (x, y),
                10,
                (0, 0, 255),
                cv2.FILLED
            )

        else:
            drawing.reset_previous()
            clear_done = False

        frame = drawing.show_canvas(frame)

        frame = draw_toolbar(frame)

        cv2.putText(
            frame,
            f"Mode: {gesture} | Tool: {current_tool}",
            (20, 445),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Shape: {detected_shape} | D Detect | S Save | U Undo | R Redo | C Clear | Q Quit",
            (20, 470),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2
        )

        cv2.imshow("AirDraw AI", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        elif key == ord("s"):
            save_drawing(drawing.canvas)

        elif key == ord("u"):
            drawing.undo()

        elif key == ord("r"):
            drawing.redo()

        elif key == ord("d"):
            detected_shape = detect_shape(drawing.canvas)
            print("Detected Shape:", detected_shape)

        elif key == ord("c"):
            drawing.clear()
            detected_shape = "None"

        elif key == ord("1"):
            drawing.draw_circle()

        elif key == ord("2"):
            drawing.draw_rectangle()

        elif key == ord("3"):
            drawing.draw_line()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()