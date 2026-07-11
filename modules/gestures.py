import math

class GestureDetector:
    def __init__(self):
        self.last_gesture = "PAUSE"
        self.stable_count = 0
        self.required_frames = 6

    def distance(self, p1, p2):
        return math.hypot(p1[1] - p2[1], p1[2] - p2[2])

    def finger_up(self, lm, tip, pip):
        return lm[tip][2] < lm[pip][2]

    def raw_gesture(self, lm):
        if not lm:
            return "PAUSE"

        index = self.finger_up(lm, 8, 6)
        middle = self.finger_up(lm, 12, 10)
        ring = self.finger_up(lm, 16, 14)
        pinky = self.finger_up(lm, 20, 18)

        up_count = sum([index, middle, ring, pinky])
        thumb_index_dist = self.distance(lm[4], lm[8])

        if up_count == 0:
            return "CLEAR"

        if index and middle and not ring and not pinky:
            return "SELECT"

        if index and middle and ring and pinky:
            return "PAUSE"

        if thumb_index_dist < 60:
            return "DRAW"

        if index and not middle and not ring and not pinky:
            return "DRAW"

        return "PAUSE"

    def detect(self, landmarks):
        gesture = self.raw_gesture(landmarks)

        if gesture == self.last_gesture:
            self.stable_count += 1
        else:
            self.last_gesture = gesture
            self.stable_count = 0

        if self.stable_count >= self.required_frames:
            return gesture

        return "PAUSE"