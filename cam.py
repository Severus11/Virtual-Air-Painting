import cv2
import os 
import track_hands as TH

header_img = "Images"
header_img_list = os.listdir(header_img)

class VideoCamera():
    def __init__(self, xp=0, yp=0,overlay_image=[], 
    draw_color =(255,200,100), x1=0, y1=0, x2=0, y2=0):
        self.xp =xp
        self.yp =yp
        self.x1 = x1
        self.y1 = y1
        self.x2= x2
        self.y2 = y2
        self.overlay_image = overlay_image  
        self.draw_color = draw_color
        self.detector = TH.handDetector(min_detection_confidence=0.85)

    def __del__(self):
        self.video.release()

    def overlay_set(self, overlay_image, header_img_list):
        for i in header_img_list:
            image = cv2.imread(f'{header_img}/{i}')
            overlay_image.append(image)
        
        return overlay_image
    
    def next_step(self, overlay_image, )


    
    def conv(self,input_image):
        frame = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
        return frame

def main():
    print('video')
    cap = cv2.VideoCapture(0)
    while True:
        ret, input_img = cap.read()
        input_img = cv2.flip(input_img,1)
        overlay
        detector= TH.handDetector(min_detection_confidence=.85)
        


        cv2.imshow('out', frame)
        cv2.waitKey(1)
        
    
if __name__ =="__main__" :
    main()
    