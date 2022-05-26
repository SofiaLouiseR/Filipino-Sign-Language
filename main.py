from flask import Flask, render_template, Response, redirect, request

import cv2  as cv2

import predict as pm


# cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)

# print( pm.predict_sign('paalam', 1,cap))

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("learn.html")
# -----------------
def gen(camera):
    while True:
        frame=camera.get_frame()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')


@app.route('/video')

def video():
    from camera import Video
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

# -----------------
# @app.route('/do_something')
# def do_something():
#   print('asdasdas')
# #   your code

#   return redirect(request.referrer)



@app.route("/learn")
def learn():
    from camera import Video
    Video.__del__(Video())
    return render_template("learn.html")

@app.route('/practice')
def practice():
    return render_template("practice.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/predict', methods=['POST'])
def predict():
    
    # print(request.form.get('word'))
    _word = request.form.get('word')
    from camera import Video
    print( pm.predict_sign(_word, 1,Video.get_cap()))
    
    return ('', 204)  




    
if __name__ == "__main__":
    app.run(debug=True)