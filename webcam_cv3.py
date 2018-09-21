import cv2
import sys
import math
import logging as log
import datetime as dt
import numpy as np
from time import sleep

cascPath = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture(0)
anterior = 0

col = [0,0,0,0,0]

height=0
width=0
divCol=5
propPixel = 1



def identificarColuna(x):
    global width
    escop = width/divCol
    global col
    if(x <= escop):
        col[0]+=1
    elif(x <= escop*2):
        col[1]+=1
    elif(x <= escop*3):
        col[2]+=1
    elif(x <= escop*4):
        col[3]+=1
    elif(x <= escop*5):
        col[4]+=1

def exibi():
    print("COL1: "+str(col[0])+"\nCOL2: "+str(col[1])+"\nCOL3: "+str(col[2])+"\nCOL4: "+str(col[3])+"\nCOL5: "+str(col[4]))

def obterAngulo(xrb, yrb, xcol, ycol):
    vetor_u = [0-xrb, 0-yrb]
    vetor_v = [xcol-xrb, ycol-yrb]
    print vetor_u
    print vetor_v
    #Angulo entre vetores cos(u,v)=u.v/|u|*|v|
    escalar_v_u = vetor_u[0]*vetor_v[0]+vetor_u[1]*vetor_v[1]
    print escalar_v_u
    modulo_u = math.sqrt(pow(vetor_u[0], 2) + pow(vetor_u[1], 2))
    modulo_v = math.sqrt(pow(vetor_v[0], 2) + pow(vetor_v[1], 2))
    print modulo_u
    print modulo_v
    angulo = escalar_v_u/(modulo_u*modulo_v)
    print math.acos(angulo)

def colunaMaisFaces():
    indexValorMax = - 1
    valorMax = -1
    for i in range(len(col)):
        if col[i] >= valorMax:
            valorMax = col[i]
            indexValorMax = i
            if valorMax == 0 and indexValorMax == divCol-1:
                return int(divCol/2)
    return indexValorMax+1



if not video_capture.isOpened():
    print('Ative a camera')
    sleep(5)
    pass

# Capture frame-by-frame
ret, frame = video_capture.read()

#frame = cv2.imread('img.jpg')

height, width = frame.shape[:2]
print("Lagura: " + str(width) + " Altura: "+ str(height))
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
)

# Desenha um retangulo em volta do rosto
for (x, y, w, h) in faces:
    identificarColuna(x)
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

if anterior != len(faces):
    anterior = len(faces)
    log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))


# Mostra resultado na tela
#cv2.imshow('Video', frame)

# Display the resulting frame
#cv2.imshow('Video', frame)
exibi()
c = colunaMaisFaces()
print "COluna mais face: " + str(c)
obterAngulo(0, -15, ((width/divCol)*c)*propPixel, -15)
cv2.imwrite("img_detect.jpg", frame)

# Libera a camera
video_capture.release()
cv2.destroyAllWindows()
