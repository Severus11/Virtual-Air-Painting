import cv2
import numpy as np

tracker = cv2.TrackerCSRT_create()
tracker_name = str(tracker).split()[0][1:]
cap = cv2.VideoCapture(0)
ret,frame = cap.read()

trackpt=[]

roi = cv2.selectROI(frame, False)
ret = tracker.init(frame, roi)
#mask = np.zeros_like(frame)

while True:
    ret, frame = cap.read()
    success, roi = tracker.update(frame)
    (x,y,w,h) = tuple (map(int, roi))
    if success:
        pts1= (x,y)
        pts2= (x+w, y+h)
        ctx= int((2*x+w)/2)
        cty = int((2*y+h)/2)
        #ct= int(((2*x+w)/2, (2*y+h)/2)) 
        #cv2.circle(frame, int(ct), 5,(255,25,0),3)
        ct = (ctx,cty)
        trackpt.append(ct)
    else:
        cv2.putText(frame, ' Failed to track',(100,200), cv2.FONT_HERSHEY_SIMPLEX,1,(25,125,255),3)
    for i in range(1, (len(trackpt)-1)):
        for j in range(2, len(trackpt)):
            if trackpt[j-1] is None or trackpt[j] is None:
                continue
            cv2.line(frame, trackpt[j-1], trackpt[j], (0,0,255),4)
        continue
   
    cv2.putText(frame,tracker_name,(20,400),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),3)
    cv2.imshow(tracker_name,frame)   
    if cv2.waitKey(50) & 0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()  
