#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

import rospy

import cv2
import sys
import math
import logging as log
import datetime as dt
import numpy as np
from time import sleep
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

cascPath = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture(0)
anterior = 0
abertHor = 62.2
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

def obterAngulo(c):
    if c == 1:
        return (abertHor/2)*-1
    elif c == 2:
        return (abertHor/4)*-1
    elif c == 3:
        return 0
    elif c == 4:
        return abertHor/4
    elif c == 5:
        return abertHor/2
    

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

def main():
    if not video_capture.isOpened():
        print('Ative a camera')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    #frame = cv2.imread('img.jpg')

    global height, width
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

    global anterior
    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))


    # Mostra resultado na tela
    #cv2.imshow('Video', frame)

    # Display the resulting frame
    #cv2.imshow('Video', frame)
    exibi()
    c = colunaMaisFaces()
    print "Coluna mais face: " + str(c)
    print(obterAngulo(c))
    cv2.imwrite("img_detect.jpg", frame)

    # Libera a camera
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
