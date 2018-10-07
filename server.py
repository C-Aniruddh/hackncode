from flask import Flask, render_template, url_for, request, session, redirect, send_from_directory, jsonify
import os
from flask_pymongo import PyMongo
import bcrypt
import datetime
import json
import re
import time
import subprocess
import threading
import random
import requests


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(APP_ROOT, 'static/downloads')

app.config['MONGO_DBNAME'] = 'hackncode'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/hackncode'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.secret_key = 'mysecret'

mongo = PyMongo(app)


@app.route('/')
def index():
    page_id = random.randint(0, 100)
    skip_id = random.randint(0, 100)
    
    host = "http://fortunecookieapi.herokuapp.com/v1/fortunes?limit=1&skip=%s&page=%s" % (skip_id, page_id)
    r = requests.get(host)
    data = r.json()
    data = list(data)

    message = data[0]['message']
    return render_template('index.html', fortune_cookie=message)


@app.route('/search')
def search():
    return 'ok'


@app.route('/new_question', methods=['POST', 'GET'])
def new_question():
    if request.method == 'POST':
        questions = mongo.db.questions
        count_all_f = questions.find({})
        count_all = count_all_f.count()
        q_id = str(count_all + 1)
        message = request.form.get('message')
        title = request.form.get('title')
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        questions.insert({'q_id' : q_id, 'message' : message, 'title' : title, 'date' : date})
        return redirect('/forum')
    return render_template('add_question.html')


@app.route('/forum')
def forum():
    questions = mongo.db.questions
    find_all = questions.find({})
    questionlist = range(0, find_all.count(), 1)
    questions_list = []
    que_id = []

    if find_all.count() > 0:
        for q in find_all:
            question_id = q['q_id']
            question_title = q['title']
            que_id.append(question_id)
            questions_list.append(question_title)

    return render_template('forum.html', question_title=question_title, questions=questions_list, que_id=que_id, questionlist=questionlist)

@app.route('/view_question/<que_id>')
def view_question(que_id):
    questions = mongo.db.questions
    comments = mongo.db.comments
    current_question = questions.find_one({'q_id' : str(que_id)})
    content = current_question['message']
    title = current_question['title']
    date = current_question['date']
    comments_post = comments.find({'que_id' : que_id})
    commentlist = range(0, comments_post.count(), 1)
    num_comment = comments_post.count()
    comment_content = []
    comment_time = []

    if comments_post.count() > 0:
        for c in comments_post:
            con = c['comment_content']
            date = c['comment_time']
            comment_content.append(con)
            comment_time.append(date)
    return render_template('view.html', que_id=que_id, question_title=title, question_content=content, question_date=date, commentlist=commentlist, comment_date=comment_time, comment_content=comment_content, num_comments=num_comment)



@app.route('/games')
def games():
    return render_template('games.html')
    
@app.route('/new_comment/<que_id>', methods=['POST'])
def new_comment(que_id):
    comments = mongo.db.comments
    comment_content = request.form.get('message')
    comment_que = que_id
    comment_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    comments.insert({'que_id' : comment_que, 'comment_content' : comment_content, 'comment_time' : comment_timestamp})
    return redirect('/forum')

# Login and registration
@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'username' in session:
        return redirect('/')
    if request.method == 'POST':
        users = mongo.db.users
        user_fname = request.form.get('name')
        # user_fname = request.form['name']
        user_email = request.form.get('email')
        existing_user = users.find_one({'name': request.form.get('username')})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form.get('password').encode('utf-8'), bcrypt.gensalt())
            users.insert(
                {'fullname': user_fname, 'email': user_email, 'name': request.form.get('username'),
                 'user_type': 'faculty', 'password': hashpass})
            session['username'] = request.form.get('username')
            return redirect('/')

        return 'A user with that Email id/username already exists'

    return render_template('register.html')


@app.route('/userlogin', methods=['POST', 'GET'])
def userlogin():
    if 'username' in session:
        return redirect('/')

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form.get('password').encode('utf-8'), login_user['password']) == login_user[
            'password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'


@app.route('/mobile/login', methods=['POST', 'GET'])
def mobilelogin():
    print("Username : " + str(request.form['username']) + "   Password : " + str(request.form['password']))
    users = mongo.db.users
    login_user = users.find_one({'email' : request.form['username']})
    if login_user is None:
       print("Returning invalid email")
       return json.dumps({'login' : 'successful'})
    print(login_user)
    login_username = login_user['name']
    login_fullname = login_user['name']

    if login_user:
       print("Inside login_user")
       if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8'))==login_user['password'].encode('utf-8'):
            print("Inside bcrypt")
            return json.dumps({'login' : 'success'})#return redirect(url_for('index'))
    return json.dumps({'login': 'unsuccessful'})


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


@app.errorhandler(404)
def error404(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error500(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)