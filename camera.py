import cv2
global cap 
# cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap = cv2.VideoCapture(0)
class Video(object):
    def __init__(self):
        # self.cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
        pass
    def __del__(self):
        try:
            self.cap.release()
            self.cap.stream.release()
        except:
            print('') #no cap yet

    def get_frame(self):
        ret,frame=cap.read()
        ret,jpg=cv2.imencode('.jpg',frame)
        # try:
        #     ret,jpg=cv2.imencode('.jpg',frame)
        # except:
        #     print('error in cam')
        #     jpg= cv2.imread('Template ver2.1.png')
        #     cap.release()
        #     cv2.destroyAllWindows()
        #     cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
        return jpg.tobytes()
    def get_cap():
        return cap


