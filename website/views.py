from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from .models import Note
from sklearn.utils import shuffle
from . import db
import json

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
        case "Panahon":
            return shuffle(["ngayon","gabi","magandang","umaga","walang hanggan","magpakailanman","hinaharap","kasalukuyan","kahapon","bukas","ngayong araw","araw-araw","madalas","kamakailan","mamaya","huli na","maaga","malapit na","paglubog ng araw","pagsikat ng araw","tanghali","hapon","minsan","dalawang beses","tatlong beses","segundo","minuto","oras","isang","dalawang","tatlong"])
        case "Pamilya":
            return shuffle(["pamilya","mama"])


@views.route('/checkAnswer', methods=['POST', 'GET'])
def process_qt_calculation():
    if request.method == "POST":
        qtc_data = request.get_json()
        print(qtc_data)
        # Dito i-return yung sagot, naka-json para hindi mag-refresh, unless need na mag-reload ang page, saka palitan ng render_template
    results = {'processed': 'true'}
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
