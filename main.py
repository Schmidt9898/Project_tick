from cam import WebcamVideoStream
from handDetector import handsDetector
import cv2
from Game_app import Game



width = 640
height = 480
#vs = WebcamVideoStream().start()
#hands = handsDetector()
tw = Game(width, height,"Tick tack toe")

tw.start_loop()

#prevHandState = ""
#hands.getHandAction(frame)
## get cursor position in open gesture
#if(prevHandState == "Closed" and hands.state == "Open"):
#    tw.putCursor = True
#    tw.cursorPosition = hands.cursorPosition
#tw.render_frame()
##cv2.imshow('webcam', frame)
## if cv2.waitKey(1) == 27 :
##    break
#prevHandState = hands.state

