import cv2
import numpy as np
import imutils

pts=[]

cap= cv2.VideoCapture(0)
while True:
    ret,  frame= cap.read()
    r1= np.array([29,86,6])
    r2= np.array([64,255,255])

    hsv= cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask= cv2.inRange(hsv,r1,r2)
    mask= cv2.erode(mask, None, iterations=2)
    mask=cv2.dilate(mask, None, iterations=2)

    contours= cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours= contours[0] if imutils.is_cv2() else contours[1]
    center= None
    if len(contours)>0:
        c= max(contours, key=cv2.contourArea)
        ((x,y), radius)= cv2.minEnclosingCircle(c)
        M= cv2.moments(c)
        #cx= int(M["m10"]/M["m00"])
        #cy=int(M["m01"]/M["m00"])
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius>10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255),2)
            cv2.circle(frame,center,5,(0,0,255),-1)
        pts.append(center)

    for i in range(1, (len(pts)-1)):
        for j in range(2,len(pts)):
            if pts[j-1] is None or pts[j] is None:
                continue
            cv2.line(frame, pts[j-1], pts[j], (0,0,255), 4)
        continue
    cv2.imshow('frame', frame)
    k= cv2.waitKey(30) & 0xff
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()
            

    
    
