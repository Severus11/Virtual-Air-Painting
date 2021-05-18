import cv2
import numpy as np
import time
import os 

import track_hands as TH

header_img = "Images"
header_img_list = os.listdir(header_img)
overlay_image =[]


for i in header_img_list:
    image = cv2.imread(f'{header_img}/{i}')
    overlay_image.append(image)

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

default_overlay= overlay_image[0]

detector= TH.handDetector(min_detection_confidence=.85)


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    frame[0:125,0:1280] = default_overlay

    frame = detector.findHands(frame, draw=False)
    landmark_list = detector.findPosition(frame, draw =False)
    if(len(landmark_list)!=0):
        x1, y1 =(landmark_list[8][1:]) #index
        x2, y2 = landmark_list[12][1:] #middle    
    cv2.imshow('paint', frame)
    cv2.waitKey(1)

