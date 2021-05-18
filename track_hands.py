import cv2
import time
import mediapipe as mp 

class handDetector():
    def __init__(self, image_mode= False, max_num_hands =3, min_detection_confidence =0.5, min_tracking_confidence =0.5):
        self.image_mode = image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        
        self.mphands= mp.solutions.hands
        self.hands = self.mphands.Hands(self.image_mode, self.max_num_hands, self.min_detection_confidence, self.min_tracking_confidence)
        self.mpdraw = mp.solutions.drawing_utils 
        self.finger_tip_id= [4,8,12,16,20]
        

    def findHands(self, img, draw =True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if  self.results.multi_hand_landmarks:
            for i in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img, i , self.mphands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, hand_num =0, draw = True):
        self.lm_list=[]
        if self.results.multi_hand_landmarks:
            myHand= self.results.multi_hand_landmarks[hand_num]
            for id, lm in enumerate(myHand.landmark):
                #print(id, lm)
                h, w, c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                self.lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, center=(cx,cy),radius=3, color=(255,255,255), thickness=1)
        return self.lm_list

    def fingerStatus(self):
        #if len(self.lm_list)!=0:    
        fingers=[]

        if (self.lm_list[self.finger_tip_id[0]][1] < self.lm_list[self.finger_tip_id[0] - 1][1]):
            fingers.append(1)
        else:
            fingers.append(0)
        
        for i in range(1,5):
            if (self.lm_list[self.finger_tip_id[i]][2] < self.lm_list[self.finger_tip_id[i] - 2][2]):
                fingers.append(1)
            else:
                fingers.append(0)
                
        return fingers


def main():
    cap = cv2.VideoCapture(0)
    previousT = 0
    currentT= 0

    detector = handDetector()

    while True:
        ret, img = cap.read()

        img =detector.findHands(img, draw=True)
        landmark_list = detector.findPosition(img)
        if len(landmark_list)!=0:
            print(landmark_list[2])

        currentT = time.time()
        fps = 1/(currentT- previousT)
        previousT = currentT

        cv2.putText(img, 'Client FPS:' + str(int(fps)), (10,70), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(255,0,0))
        cv2.imshow('img', img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()