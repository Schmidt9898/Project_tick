
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
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)


class handsDetector:
    def __init__(self, hold_time = 1.5):
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
        
        if self.isAction:
            #print("clear time")
            self.start_time=time.time()
        self.isAction=False

        #process image
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        self.height, self.width = image.shape[:2]
        #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                tTip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                tTip = (tTip.x*float(self.width), tTip.y*float(self.height))
                #print(tTip)
                self.cursorPosition = tTip
                #print("distance",distance(tTip,self.startPosition))
                if self.distance_treshold>distance(tTip,self.startPosition):
                    if self.start_time+self.holdTime<=time.time():
                        #print("is this true")
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
        return [self.cursorPosition[0]/self.width, self.cursorPosition[1]/self.height]
