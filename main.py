from cam import WebcamVideoStream
from handDetector import handsDetector
import cv2
from Game_app import Game

tw = Game(640, 480,"Tick tack toe")
tw.start_loop()

