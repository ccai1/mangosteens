from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
import os

from passlib.hash import sha256_crypt

import db_edit

app = Flask(__name__)
app.secret_key = os.urandom(8)


@app.route('/')
def home():
    ''' this function loads up home session, from where user can login and navigate through the website'''
    #checks if there is a session
    if 'user' in session:
        #if there is then just show the welcome screen
        return render_template('welcome.html', user=session['user'])
    else:
        #if not just ask for info
        return render_template('home.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    '''logs the user in by checking if their login info matches with registered user'''
    username = request.form['usr'].strip()
    password = request.form['pwd'].strip()
    user_exists = db_edit.findInfo('users', db_edit.checkApos(username), 'username', fetchOne = True)
    '''find password for username'''
    if user_exists:
        print (sha256_crypt.verify(password, user_exists[3]))
        if sha256_crypt.verify(password, user_exists[3]):
            session['user'] = username
            return redirect(url_for('home'))
        else:
            flash("password wrong")
            return render_template('home.html')
    flash("username wrong")
    return redirect(url_for('home'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    '''registers new account for user'''
    password = request.form['new_pwd'].strip()
    username= request.form['new_usr'].strip()
    pwdCopy = request.form['re_pwd'].strip()
    if username.find("'") == -1:
            if password == pwdCopy:
                db_edit.insert('users', [username, sha256_crypt.encrypt(password), ''])
                '''insert username and password into database'''
                flash("registration complete, please re-enter your login info");
            else:
                flash('passwords do not match')
    else:
        flash("pick a username without apostrophes")
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    '''pops user from session, brings user back to home page'''
    session.pop('user')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
