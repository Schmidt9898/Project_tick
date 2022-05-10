
import cv2
import mediapipe as mp
import numpy as np
import math
from itertools import permutations
import datetime

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


class handsDetector:
    def __init__(self, hold_time = 2):
        self.hands = mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

        self.stateCount = 0
        self.state = "Unknown"
        self.height = 0
        self.width = 0
        self.holdTime= hold_time
        self.cursorPosition = [0,0]
        self.boardPosition = 0
        self.closedTime = datetime.datetime
        #0 no hold - 1 hold  - 2 hold-press - 3 hold-pressed
        self.holdStatus = 0

    def getHandAction(self, frame):

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_world_landmarks:
          for hand_landmarks in results.multi_hand_world_landmarks:
                tTip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                tTip = [tTip.x, tTip.y]
                iTip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                iTip = [iTip.x, iTip.y]

                dist = math.dist(tTip, iTip)
                self.height, self.width = image.shape[:2]

                if(dist< 0.05):
                    if self.state != "Closed":
                        self.stateCount += 1

                        if self.stateCount == 10:
                             self.state = "Closed"
                             self.closedTime = datetime.datetime.now()
                             self.stateCount = 0
                else:
                    if self.state != "Open":
                        self.stateCount += 1

                        if self.stateCount == 10:
                             self.state = "Open"
                             self.stateCount = 0

                if self.state == "Closed":
                    timeclosed = (datetime.datetime.now() - self.closedTime).total_seconds()
                    if timeclosed < self.holdTime:
                        self.holdStatus = 1
                    elif timeclosed > self.holdTime and self.holdStatus == 1:
                        self.holdStatus = 2
                    else:
                        self.holdStatus = 3
                else:
                    self.holdStatus = 0


        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                tTip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                tTip = [tTip.x*self.width, tTip.y*self.height]

                self.cursorPosition = tTip

    def getBoardPosition(self):
        return [self.cursorPosition/self.width, self.cursorPosition/self.height]
