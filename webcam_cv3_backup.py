import cv2
import sys
import logging as log
import datetime as dt
import numpy as np
from time import sleep

cascPath = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
eye_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_eye.xml')
log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture(0)
anterior = 0

col1=0
col2=0
col3=0
col4=0
col5=0



def identificarColuna(x, width):
    escop = width/5
    global col1, col2, col3, col4, col5
    if(x <= escop):
        col1+=1
        return 1
    elif(x <= escop*2):
        col2+=1
        return 2
    elif(x <= escop*3):
        col3+=1
        return 3
    elif(x <= escop*4):
        col4+=1
        return 4
    elif(x <= escop*5):
        col5+=1
        return 5

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()
    height, width = frame.shape[:2]
    print("Lagura: " + str(width) + " Altura: "+ str(height))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        print(str(x) + ":" + str(h))
        print(identificarColuna(x, width))
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))


    # Display the resulting frame
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()