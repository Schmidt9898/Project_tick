from cam import WebcamVideoStream
from handDetector import handsDetector
import cv2
from Game_app import Game

if __name__ == "__main__":
    tw = Game(640, 480,"Tick tack toe")
    tw.start_loop()

