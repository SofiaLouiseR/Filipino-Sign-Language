import cv2

class Video(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
    def __del__(self):
        self.cap.release()
    def get_frame(self):
        ret,frame=self.cap.read()
        ret,jpg=cv2.imencode('.jpg',frame)
        return jpg.tobytes()
    def get_cap(self):
        return self.cap

