import cv2
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
class Video(object):
    def __init__(self):
        # self.cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
        pass
    def __del__(self):
        cap.release()
    def get_frame(self):
        ret,frame=cap.read()
        ret,jpg=cv2.imencode('.jpg',frame)
        return jpg.tobytes()
    def get_cap():
        return cap

