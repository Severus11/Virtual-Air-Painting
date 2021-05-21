import cv2
import track_hands as TH
import os 
import time 
import numpy as np


brush_thickness = 15
eraser_thickness = 100
image_canvas =np.zeros((720,1280,3), np.uint8)

header_img = "Images"
header_img_list = os.listdir(header_img)
overlay_image =[]


for i in header_img_list:
    image = cv2.imread(f'{header_img}/{i}')
    overlay_image.append(image)

detector= TH.handDetector(min_detection_confidence=.85)

class VideoCamera():
    def __init__(self, xp=0, yp=0, currentT=0,previousT =0, 
    default_overlay= overlay_image[0], draw_color =(255,200,100), x1=0, y1=0, x2=0, y2=0):
        self.video= cv2.VideoCapture(0)
        self.video.set(3,1280)
        self.video.set(4,720)
        self.xp =xp
        self.yp =yp
        self.x1 = x1
        self.y1 = y1
        self.x2= x2
        self.y2 = y2
        self.currentT = currentT
        self.previousT = previousT
        self.default_overlay= default_overlay
        self.draw_color = draw_color

    def __del__(self):
        self.video.release()
    
    def ret_frame(self):
        _, frame = self.video.read()
        frame = cv2.flip(frame,1)
        frame[0:125,0:1280] = self.default_overlay

        frame = detector.findHands(frame, draw=True)
        landmark_list = detector.findPosition(frame, draw =False)

        if(len(landmark_list)!=0):
            self.x1, self.y1 =(landmark_list[8][1:]) #index
            self.x2, self.y2 = landmark_list[12][1:] #middle    
        
            my_fingers = detector.fingerStatus()
            #print(my_fingers)
            if (my_fingers[1]and my_fingers[2]):
                self.xp, self.yp = 0,0
                if (self.y1<125):
                    if(200<self.x1<340):
                        self.default_overlay = overlay_image[0] 
                        self.draw_color = (255,0,0)
                    elif (340<self.x1<500):
                        self.default_overlay = overlay_image[1]
                        self.draw_color = (47,225,245)
                    elif (500<self.x1<640):
                        self.default_overlay = overlay_image[2]
                        self.draw_color = (197,47,245)
                    elif (640<self.x1<780):
                        self.default_overlay = overlay_image[3]
                        self.draw_color = (53,245,47)
                    elif (1100<self.x1<1280):
                        self.default_overlay = overlay_image[4]
                        self.draw_color = (0,0,0)

                cv2.putText(frame, 'Color Selector Mode', (900,680), fontFace=cv2.FONT_HERSHEY_COMPLEX, color= (0,255,255), thickness=2, fontScale=1)
                cv2.line(frame, (self.x1,self.y1), (self.x2,self.y2), color=self.draw_color, thickness=3)

            if (my_fingers[1] and not my_fingers[2]):
                        
                cv2.putText(frame, "Writing Mode", (900,680), fontFace= cv2.FONT_HERSHEY_COMPLEX, color= (255,255,0), thickness=2, fontScale=1)
                cv2.circle(frame, (self.x1,self.y1),15, self.draw_color, thickness=-1)

                if self.xp ==0 and self.yp ==0:
                    self.xp =self.x1 
                    self.yp =self.y1
                
                if self.draw_color == (0,0,0):
                    cv2.line(frame, (self.xp,self.yp),(self.x1,self.y1),color= self.draw_color, thickness=eraser_thickness)
                    cv2.line(image_canvas, (self.xp,self.yp),(self.x1,self.y1),color= self.draw_color, thickness=eraser_thickness)

                else:
                    cv2.line(frame, (self.xp,self.yp),(self.x1,self.y1),color= self.draw_color, thickness=brush_thickness)
                    cv2.line(image_canvas, (self.xp,self.yp),(self.x1,self.y1),color= self.draw_color, thickness=brush_thickness)
                
                self.xp , self.yp = self.x1, self.y1

        img_gray = cv2.cvtColor(image_canvas, cv2.COLOR_BGR2GRAY)
        _, imginv= cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
        imginv = cv2.cvtColor(imginv, cv2.COLOR_GRAY2BGR)
        frame = cv2.bitwise_and(frame, imginv)
        frame =cv2.bitwise_or(frame, image_canvas)
        self.currentT = time.time()
        self.fps = 1/(self.currentT- self.previousT)
        self.previousT = self.currentT
        
        return frame, self.fps


def main():
    my_paint = VideoCamera()
    while True:
        my_frame, my_fps = my_paint.ret_frame()
        
        cv2.putText(my_frame, 'Client FPS:' + str(int(my_fps)), (10,670), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0), thickness=2)
        cv2.imshow('paint', my_frame)


if __name__ == "__main__":
    main()