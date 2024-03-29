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

import requests
import random
import cloudinary
import cloudinary.uploader


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(APP_ROOT, 'static/downloads')


cloudinary.config(
  cloud_name = 'dcdbkpkx1',  
  api_key = '268162775417963',  
  api_secret = 'tkKUNITB977O6xrH4XDnexYJPk4'  
)


app.config['MONGO_DBNAME'] = 'hackncode'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/hackncode'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.secret_key = 'mysecret'

mongo = PyMongo(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if 'username' in session:
        page_id = random.randint(0, 100)
        skip_id = random.randint(0, 100)
        image_id = random.randint(0, 1000)

        host = "http://fortunecookieapi.herokuapp.com/v1/fortunes?limit=1&skip=%s&page=%s" % (skip_id, page_id)
        r = requests.get(host)
        data = r.json()
        data = list(data)

        message = data[0]['message']

        """
        random_img = "https://picsum.photos/g/512/512/?image=%s" % image_id
        print(random_img)
        file_name = "%s.jpg" % image_id 
        r = requests.get(random_img, stream = True)
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size = 1024*1024):
                if chunk:
                    f.write(chunk)

        upload_url = cloudinary.uploader.upload(file_name)['url']
        file_name_remote = upload_url.split('/')[-1]
        print(upload_url)
        # imgurl = cloudinary.CloudinaryImage(file_name_remote).image(overlay={'font_family': "Arial", 'font_size': 24, 'font_weight': "bold", 'text', 'font_color' : "white" : str(message)})

        imgurl = "http://res.cloudinary.com/dcdbkpkx1/image/upload/l_text:Arial_24_bold:%s,co_rgb:eee/%s" % (message, file_name_remote)
        print(imgurl)
        """

        return render_template('index.html', fortune_cookie=message)
    else:
        return redirect('/userlogin')

# Login and register 
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
                 'user_type': 'worker', 'password': hashpass})
            session['username'] = request.form.get('username')
            return redirect('/')

        return 'A user with that Email id/username already exists'

    return render_template('signup.html')

@app.route('/voice_call/<query>', methods=['POST', 'GET'])
def voice_call(query):
    print(query)
    
    return 'hi'

@app.route('/search', methods=['POST', 'GET'])
def search():
    return str('Hi')

@app.route('/userlogin', methods=['POST', 'GET'])
def userlogin():
    if 'username' in session:
        return redirect('/')

    return render_template('signin.html')


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form.get('password').encode('utf-8'), login_user['password']) == login_user[
            'password']:
            session['username'] = request.form['username']
            return redirect('/')

    return 'Invalid username/password combination'


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/mobile/login', methods=['POST', 'GET'])
def mobilelogin():
    print("Username : " + str(request.form['username']) + "   Password : " + str(request.form['password']))
    global login_flag
    users = mongo.db.users
    login_user = users.find_one({'email' : request.form['username']})
    if login_user is None:
       print("Returning invalid email")
       return json.dumps({'login' : 'successful'})
    print(login_user)
    login_username = login_user['name']
    login_fullname = login_user['name']
    login_mail = login_user['email']
    login_user_type = login_user['user_type']

    if login_user:
       print("Inside login_user")
       if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8'))==login_user['password'].encode('utf-8'):
            print("Inside bcrypt")
            auth_token = str(bcrypt.hashpw(auth_string.encode('utf-8'), bcrypt.gensalt()))
            print("Auth token :  " +  str(auth_token))
            login_flag = 1#session['username'] = request.form['username']
            return json.dumps({'login_background' : login_background, 'login_identifier' : login_identifier, 'login_committee' : login_committee, 'auth_token' : auth_token, 'login' : 'success', 'email':login_mail, 'username':login_username, 'fullname' : login_fullname, 'type':login_user_type})#return redirect(url_for('index'))
    return json.dumps({'login': 'unsuccessful'})








@app.route('/downloads/<filename>')
def downloads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_unresponsive(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0')
