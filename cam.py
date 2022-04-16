print("cam.py")
import cv2 as cv 


cam = cv.VideoCapture(0)   
s, img = cam.read()
if s:
    cv.namedWindow("cam-test")
    cv.imshow("cam-test",img)
    cv.waitKey(0)
    cv.destroyWindow("cam-test")
    cv.imwrite("filename.jpg",img)