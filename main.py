import cv2
from modules.hand_tracker import HandTracker
from modules.drawing import DrawingCanvas

def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    drawing = DrawingCanvas()

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        frame, landmarks = tracker.find_hand(frame)

        if landmarks:
            x, y = landmarks[8][1], landmarks[8][2]
            frame = drawing.draw(frame, x, y)
            cv2.circle(frame, (x, y), 10, (0, 0, 255), cv2.FILLED)
        else:
            drawing.reset_previous()

        cv2.putText(frame, "Press C to Clear | Press Q to Quit", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("AirDraw AI", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("c"):
            drawing.clear()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()