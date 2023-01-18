from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask import Response
from flask_login import login_required, current_user
from .models import Note
from sklearn.utils import shuffle
from . import db
import json
# import cv2
import predict as pm
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


# @views.route('/quiz', methods=['GET', 'POST'])
# @login_required
# def quiz():
#     topic = session['topic']
#     words = session['words']
#     if topic == "":
#         topic = "none"
#     print(topic)
#     print(words)
#     return render_template("quiz.html", user=current_user, topic=topic, words=words)


@views.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if request.method == 'POST':
        topic = request.form.get('topic')
        words = getWords(topic)
        print(topic)
    else:
        words = []
        topic = "none"
        print(topic)
        print(words)
    return render_template("quiz.html", user=current_user, topic=topic, words=words)
    # session['topic'] = topic
    # session['words'] = words
    # return render_template("quiz.html", user=current_user, topic=topic, words=words)
    # topic = session['topic']
    # words = session['words']
    # if topic == "":
    #     topic = "none"
    # print(topic)
    # print(words)
    # return render_template("quiz.html", user=current_user, topic=topic, words=words)


@views.route('/getWords')
@login_required
def getWords(topic):
    match topic:
        case "Hugis":
            return shuffle(["bituin", "parisukat", "bilog", "tatsulok"])
        case "Kulay":
            return shuffle(["itim", "puti", "kayumanggi", "violet"])
        case "Lugar":
            return shuffle(["mundo", "Maynila", "Pilipinas"])
        case "Madalas Sabihin":
            return shuffle(["ulit", "mahal kita", "hi/hello", "salamat"])
        case "Pamilya":
            return shuffle(["babae", "lalake", "kamag-anak", "matanda"])
        case "Panahon / Oras":
            return shuffle(["ngayon", "gabi", "magandang", "umaga", "kahapon"])
        case "Pandiwa":
            return shuffle(["hintay", "gusto", "tingnan", "basa"])
        case "Panghalip Pananong":
            return shuffle(["sino", "ano", "kailan", "saan"])


@views.route('/checkAnswer', methods=['POST', 'GET'])
def process_qt_calculation():
    if request.method == "POST":
        # Dito yung code para i-check ang sagot
        # TYPE HERE
        word_case =  request.get_json()
        print('json file..-' + str (word_case))
        word = word_case['currentWord']
        print('ang word ay: ' + word)

        # Ito naman yung pagbalik sa HTML ng score, naka-json para hindi mag-refresh, unless need na mag-reload ang page, saka palitan ng render_template
        # if(pm.predict_sign(word, video().Video.get_cap())):
        # if(pm.predict_sign('salamat')):
        #     score = 1
        #     print('tama predict')
        # else:
        #     score =0
        #     print('mali predict')
        score = 1 #change itong number kung anong score, 1 kung tama, 0 kung mali
        print(score)
    results = {'processed': 'true', 'score': score}
    return jsonify(results)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template("profile.html", user=current_user)


# Reference sa pag-record ng score
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


# -----------------------------------
def gen(camera):
    
    while True:
        frame=camera.get_frame() 
        yield(b'--frame\r\n'
         b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')
    


@views.route('/video')

def video():
    
    from camera import Video
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')