# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import url_for
from flask import request

import os
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        text = "Welcome %s" % request.form['username']
        headimg = url_for('static', filename='images/headimg.png')
        return '<img src="%s" /><h3>%s</h3>' % (headimg, text)
    else:
        headimg = url_for('static', filename='images/headimg.png')
        name = 'Ryan'
        l1 = ['home', 'auto', 'girl', u'装修', u'长城']
        d1 = {'birth': '19881220', 'hometown': u'河北', 'phone': '18621567233'}
        return render_template('hello.html', l1=l1, name=name, d1=d1, head=headimg)

@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    return render_template('regist.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        conn = sqlite3.connect('my.db')
        cursor = conn.cursor()
        sql = 'insert into user (username, password) values (?, ?)'
        cursor.execute(sql, (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        return '%s, %s regist & login' % (username, password)
    else:
        return render_template('login.html')

@app.route('/done/')
def over():
    url = request.args['url']
    username = request.args['username']
    return '<img src="%s"><p>%s</p>' % (url, username)

# upload file to server
@app.route('/up/', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        file_path = 'static/images'
        fn = request.files['file']
        fn.save(os.path.join(file_path, fn.filename))
        save_file = os.path.join('/',file_path, fn.filename)
        return '<img src="%s">%s has saved!' % (save_file, fn.filename)
    else:
        return render_template('upload.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)

