import cv2
import mediapipe as mp
import math
from collections import deque

class HandGestureRecognizer:
    def __init__(self, detection_confidence=0.7):
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=1,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

    def detect(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        gesture = "No Hand"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                lm_list = [(lm.x, lm.y) for lm in hand_landmarks.landmark]
                gesture = self.classify_static_gesture(lm_list)
                #self.mp_draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

        return frame, gesture

    def classify_static_gesture(self, lm):
        if len(lm) < 21:
            return "Unknown"

        finger_up = {
            "index": lm[8][1] < lm[6][1],
            "middle": lm[12][1] < lm[10][1],
            "ring": lm[16][1] < lm[14][1],
            "pinky": lm[20][1] < lm[18][1],
        }

        thumb_up = lm[4][1] < lm[3][1]
        thumb_down = lm[4][1] > lm[3][1]

        thumb_tip = lm[4]
        index_tip = lm[8]
        thumb_mid = lm[3]
        index_mid = lm[6]

        base_distance = self.distance(thumb_mid, index_mid)

        tip_distance = self.distance(thumb_tip, index_tip)

        vector_thumb = (thumb_tip[0] - thumb_mid[0], thumb_tip[1] - thumb_mid[1])
        vector_index = (index_tip[0] - index_mid[0], index_tip[1] - index_mid[1])
        dot_product = vector_thumb[0]*vector_index[0] + vector_thumb[1]*vector_index[1]
        magnitude_thumb = math.hypot(*vector_thumb)
        magnitude_index = math.hypot(*vector_index)
        cos_angle = dot_product / (magnitude_thumb * magnitude_index + 1e-6)

        angle = math.acos(min(1.0, max(-1.0, cos_angle))) * (180 / math.pi)

        other_fingers_folded = not finger_up["middle"] and not finger_up["ring"] and not finger_up["pinky"]

        if (
            base_distance < 0.08 and
            tip_distance > 0.1 and
            angle > 60 and  
            other_fingers_folded
        ):
            return "Like Song"


        if all(finger_up.values()):
            return "Pause"
        if finger_up["index"] and finger_up["middle"] and not finger_up["ring"] and not finger_up["pinky"]:
            return "Play"
        if finger_up["index"] and finger_up["pinky"] and not finger_up["middle"] and not finger_up["ring"]:
            return "Shuffle"
        if thumb_up and not any(finger_up.values()):
            return "Volume Up"
        if thumb_down and not any(finger_up.values()):
            return "Volume Down"

        return "Unknown"

    @staticmethod
    def distance(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

class FaceGestureRecognizer:
    def __init__(self, detection_confidence=0.5):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.face_positions = deque(maxlen=10)
        self.motion_lock_until = 0
        self.motion_lock_duration = 3

    def detect_face_motion(self, frame):
        current_time = cv2.getTickCount() / cv2.getTickFrequency()
        if current_time < self.motion_lock_until:
            return frame, "None"

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(img_rgb)
        gesture = "Unknown"

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                nose_tip_x = face_landmarks.landmark[1].x
                self.face_positions.append(nose_tip_x)

                '''self.mp_draw.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                    connection_drawing_spec=self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=1)
                )'''

                if len(self.face_positions) == self.face_positions.maxlen:
                    x_avg_start = sum(list(self.face_positions)[:5]) / 5
                    x_avg_end = sum(list(self.face_positions)[-5:]) / 5
                    x_diff = x_avg_end - x_avg_start
                    x_thresh = 0.10

                    if abs(x_diff) > x_thresh:
                        self.motion_lock_until = current_time + self.motion_lock_duration
                        self.face_positions.clear()
                        if x_diff > 0:
                            gesture = "Next Track"
                        else:
                            gesture = "Previous Track"

        return frame, gesture
