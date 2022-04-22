import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


class handsDetector:
    def __init__(self):
        self.hands = mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

    def getLandMarks(self, frame):

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
          for hand_landmarks in results.multi_hand_landmarks:
                print("THUMB_TIP",hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP])
                print("INDEX_FINGER_TIP",hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP])
                print("MIDDLE_FINGER_TIP",hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP])
                print("RING_FINGER_TIP",hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP])
                print("PINKY_TIP",hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP])