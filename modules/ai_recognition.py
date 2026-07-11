import cv2

def detect_shape(canvas):

    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < 500:
            continue

        peri = cv2.arcLength(cnt, True)

        approx = cv2.approxPolyDP(
            cnt,
            0.04 * peri,
            True
        )

        sides = len(approx)

        if sides == 3:
            return "Triangle"

        elif sides == 4:
            return "Rectangle"

        elif sides > 6:
            return "Circle"

    return "Unknown"