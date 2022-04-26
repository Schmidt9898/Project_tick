from cam import WebcamVideoStream
from handDetector import handsDetector
import cv2
from Gui import Game_Gui
import glfw

if __name__ == "__main__" :
    vs = WebcamVideoStream().start()
    hands = handsDetector()
    tw= Game_Gui()

    while not glfw.window_should_close(tw.window):
        try:
            frame = vs.read()
            frame=cv2.flip(frame,1) # mirror the image
            tw.set_frame(frame)
            #process by CV algorithm, GUI
            hands.getHandAction(frame)
            tw.render_frame()

            #cv2.imshow('webcam', frame)
            #if cv2.waitKey(1) == 27 :
            #    break
            #print(hands.state)

        except:
            vs.stop()
            cv2.destroyAllWindows()
            tw.impl.shutdown()
            glfw.terminate()

    tw.impl.shutdown()
    glfw.terminate()
    vs.stop()
    cv2.destroyAllWindows()