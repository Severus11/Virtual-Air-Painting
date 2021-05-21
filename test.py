import cv2


class conv2blk():
    def __init__(self, input_image):
        self.input_image = input_image
    
    def conv(self,input_image):
        frame = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
        return frame

def main():
    print('video')
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, input_img = cap.read()
        converter = conv2blk(input_img)
        frame = converter.conv(input_img)
        cv2.imshow('out', frame)
        cv2.waitKey(1)
        
    
if __name__ =="__main__" :
    main()
    