#!/usr/bin/env python

from threading import Thread, Lock
import cv2

class WebcamVideoStream :
    """Class for the video camera handler.

    .. note::

       This function is thread safe

    """
    def __init__(self, src = 0) :
        """Constructor of handsDetectorClass.

        It starts the opencv Videocapture
        :param src: source of the camera
        :type name: int
        """
        self.stream = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self) :
        """Start of the camera thread.
        """
        if self.started :
            print("already started!!")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self) :
        """This function works in a thread to update every frame constanstly
        """
        while self.started :
            (grabbed, frame) = self.stream.read()
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self) :
        """Read the last frame updated
        :returns:  mat --  Last updated frame of the camera
        """
        self.read_lock.acquire()
        frame = self.frame.copy()
        self.read_lock.release()
        return frame

    def stop(self) :
        """Stop the camera thread
        """
        self.started = False
        if self.thread.is_alive():
            self.thread.join()


    def __exit__(self, exc_type, exc_value) :
        """Release the camera stream
        """
        self.stream.release()
