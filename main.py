from cam import WebcamVideoStream
from handDetector import handsDetector
import cv2
from Gui import Game_Gui
import glfw

if __name__ == "__main__":
    width = 640
    height = 480
    vs = WebcamVideoStream().start()
    hands = handsDetector()
    tw = Game_Gui(width, height)
    prevHandState = ""
    test_array = [
        "o", "o", "",
        "x", "", "x",
        "x", "o", "",
    ]
    while not glfw.window_should_close(tw.window):
        try:
            frame = vs.read()
            frame = cv2.flip(frame, 1)  # mirror the image
            tw.set_frame(frame)
            # process by CV algorithm
            hands.getHandAction(frame)

            # get cursor position in open gesture
            if(prevHandState == "Closed" and hands.state == "Open"):
                tw.putCursor = True
                tw.cursorPosition = hands.cursorPosition
            tw.render_frame()

            #cv2.imshow('webcam', frame)
            # if cv2.waitKey(1) == 27 :
            #    break
            prevHandState = hands.state

        except:
            vs.stop()
            cv2.destroyAllWindows()
            tw.impl.shutdown()
            glfw.terminate()

    tw.impl.shutdown()
    glfw.terminate()
    vs.stop()
    cv2.destroyAllWindows()
