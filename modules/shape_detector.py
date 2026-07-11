import cv2


def detect_shape(canvas):
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return "No shape detected"

    contour = max(contours, key=cv2.contourArea)

    if cv2.contourArea(contour) < 500:
        return "Shape is too small"

    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)

    corners = len(approx)

    if corners == 3:
        return "Triangle"

    if corners == 4:
        x, y, w, h = cv2.boundingRect(approx)
        ratio = w / float(h)

        if 0.85 <= ratio <= 1.15:
            return "Square"

        return "Rectangle"

    if corners > 6:
        return "Circle"

    return "Unknown Shape"