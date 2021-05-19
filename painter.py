import cv2
import numpy as np
import time
import os 

import track_hands as TH

brush_thickness = 15
eraser_thickness = 100
image_canvas =np.zeros((720,1280,3), np.uint8)

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
draw_color = (255,200,100)

detector= TH.handDetector(min_detection_confidence=.85)

xp =0
yp=0

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    frame[0:125,0:1280] = default_overlay

    frame = detector.findHands(frame, draw=True)
    landmark_list = detector.findPosition(frame, draw =False)

    if(len(landmark_list)!=0):
        x1, y1 =(landmark_list[8][1:]) #index
        x2, y2 = landmark_list[12][1:] #middle    
    
        my_fingers = detector.fingerStatus()
        #print(my_fingers)
        if (my_fingers[1]and my_fingers[2]):
            if (y1<125):
                if(200<x1<340):
                    default_overlay = overlay_image[0] 
                    draw_color = (255,0,0)
                elif (340<x1<500):
                    default_overlay = overlay_image[1]
                    draw_color = (47,225,245)
                elif (500<x1<640):
                    default_overlay = overlay_image[2]
                    draw_color = (197,47,245)
                elif (640<x1<780):
                    default_overlay = overlay_image[3]
                    draw_color = (53,245,47)
                elif (1100<x1<1280):
                    default_overlay = overlay_image[4]
                    draw_color = (0,0,0)

            cv2.putText(frame, 'Color Selector Mode', (900,680), fontFace=cv2.FONT_HERSHEY_COMPLEX, color= (0,255,255), thickness=2, fontScale=1)
            cv2.line(frame, (x1,y1), (x2,y2), color=draw_color, thickness=3)

        if (my_fingers[1] and not my_fingers[2]):
            xp, yp = 0,0
            
            cv2.putText(frame, "Writing Mode", (900,680), fontFace= cv2.FONT_HERSHEY_COMPLEX, color= (255,255,0), thickness=2, fontScale=1)
            cv2.circle(frame, (x1,y1),15, draw_color, thickness=-1)

            if xp ==0 and yp ==0:
                xp =x1 
                yp =y1
            if draw_color == (0,0,0):
                cv2.line(frame, (xp,yp),(x1,y1),color= draw_color, thickness=eraser_thickness)
                cv2.line(image_canvas, (xp,yp),(x1,y1),color= draw_color, thickness=eraser_thickness)

            cv2.line(frame, (xp,yp),(x1,y1),color= draw_color, thickness=brush_thickness)
            cv2.line(image_canvas, (xp,yp),(x1,y1),color= draw_color, thickness=brush_thickness)
            xp , yp = x1, y1

    img_gray = cv2.cvtColor(image_canvas, cv2.COLOR_BGR2GRAY)
    _, imginv= cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    imginv = cv2.cvtColor(imginv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, imginv)
    frame =cv2.bitwise_or(frame, image_canvas)


    cv2.imshow('paint', frame)
    cv2.waitKey(1)

