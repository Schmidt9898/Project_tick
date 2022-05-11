
from cmath import sqrt
import cv2
import mediapipe as mp
import numpy as np
import math
from itertools import permutations
import datetime
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def distance(a,b):
    """Calculate euclidian distance beetween two points.

    :param a: First point.
    :type name: float.
    :param state: Second Point.
    :type state: float.
    :returns:  float -- the distance beetween a and b.

    """
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)


class handsDetector:
    """Class to handle the finger action.

    .. note::

       This class needs the MediaPipe Hands library.

    """
    def __init__(self, hold_time = 1.5):
        """Constructor of handsDetectorClass.

        :param a: time to wait for click action.
        :type name: float.
        """
        self.hands = mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

        self.height = 0
        self.width = 0
        self.holdTime= hold_time
        self.cursorPosition = (0,0)
        self.startPosition = (0,0)
        self.isAction=False
        self.distance_treshold=50.0
        self.progres=1.0
        self.start_time=time.time()


    def getHandAction(self, frame):
        """Gets the action of the hand.
        It process the movement of the fingers and detects
        if the index finger tip is holded for a while

        :param a: frame.
        :type name: mat image.

        """
        if self.isAction:
            self.start_time=time.time()
        self.isAction=False

        #process image
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        self.height, self.width = image.shape[:2]

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                tTip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                tTip = (tTip.x*float(self.width), tTip.y*float(self.height))
                self.cursorPosition = tTip
                if self.distance_treshold>distance(tTip,self.startPosition):
                    if self.start_time+self.holdTime<=time.time():
                        self.isAction=True
                    pass

                else:
                    self.startPosition=self.cursorPosition
                    self.start_time=time.time()
        else:
            self.start_time=time.time()
            pass
        self.progres=(time.time()-self.start_time) / self.holdTime




    def getBoardPosition(self):
        """Get the board position of the index finger tip.
        It process the movement of the fingers and detects
        if the index finger tip is holded for a while

        :returns:  list -- x,y coordinates of the board

        """
        return [self.cursorPosition[0]/self.width, self.cursorPosition[1]/self.height]