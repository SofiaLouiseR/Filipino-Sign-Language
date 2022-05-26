from flask import Flask, render_template, Response, redirect, request
from camera import Video
import cv2  as cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf  
import time
# from tensorflow.keras.models import Sequential 
# from tensorflow.keras.layers import LSTM, Dense 
# from tensorflow.keras.callbacks import TensorBoard 
# import prediction_model as pm
# import sentence_builder as sb



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
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

# -----------------
@app.route('/do_something')
def do_something():
  print('asdasdas')
#   your code

  return redirect(request.referrer)

@app.route('/create_file', methods=['POST'])
def create_file():
    if request.method == 'POST':
        with open(f"{request.form.get('name')}.txt", "w") as f:
            f.write('FILE CREATED AND SUCCESSFULL POST REQUEST!')
        return ('', 204)  

@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route('/practice')
def practice():
    return render_template("practice.html")

@app.route("/about")
def about():
    return render_template("about.html")
    
if __name__ == "__main__":
    app.run(debug=True)