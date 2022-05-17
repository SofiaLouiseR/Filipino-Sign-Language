from flask import Flask, render_template, Response
from camera import Video

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("learn.html")

@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route('/practice')
def practice():
    return render_template("practice.html")

def gen(camera):
    while True:
        frame=camera.get_frame()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')

def video():
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/about")
def about():
    return render_template("about.html")
    
if __name__ == "__main__":
    app.run(debug=True)