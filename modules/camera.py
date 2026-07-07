import cv2

def start_camera():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera not found.")
        return

    while True:
        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        cv2.imshow("AirDraw AI Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()