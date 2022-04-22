from cam import WebcamVideoStream
from handDetector import handsDetector
import cv2

if __name__ == "__main__" :
    vs = WebcamVideoStream().start()
    hands = handsDetector()

    while True :
        try:
            frame = vs.read()
            #process by CV algorithm, GUI
            hands.getLandMarks(frame)
            cv2.imshow('webcam', frame)
            if cv2.waitKey(1) == 27 :
                break
        except:
            vs.stop()
            cv2.destroyAllWindows()

    vs.stop()
    cv2.destroyAllWindows()