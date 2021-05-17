import cv2
import time
import mediapipe as mp 

mphands= mp.solutions.hands
hands = mphands.Hands(static_image_mode = False, max_num_hands = 3, min_detection_confidence = 0.5, min_tracking_confidence =0.5)
mpdraw = mp.solutions.drawing_utils 
cap = cv2.VideoCapture(0)

previousT = 0
currentT= 0

while True:
    ret , img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if  results.multi_hand_landmarks:
        for i in results.multi_hand_landmarks:
            mpdraw.draw_landmarks(img, i , mphands.HAND_CONNECTIONS)
    
    currentT = time.time()
    fps = 1/(currentT- previousT)
    previousT = currentT

    cv2.putText(img, 'Client FPS:' + str(int(fps)), (10,70), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0))

    cv2.imshow('img', img)
    cv2.waitKey(1)
    