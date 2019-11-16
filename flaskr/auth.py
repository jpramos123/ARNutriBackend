import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
import json

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=(['POST']))
def register():
    
    

    user_register = {
        'name': request.form['name'],
        'gender' : request.form['gender'],
        'email' : request.form['email'],
        'birth_date' : request.form['birth_date'],
        'password' : request.form['password'],
        'medicalRegister' : request.form['medicalRegister'],
        'userType' : request.form['userType']
        }

    error = None
    db = g.db
    cursor = db.cursor()

   
    for key in user_register:
        if key != 'medicalRegister':
           if user_register[key] is None:
                error =  "{} is required".format(key)


    cursor.execute(
        'SELECT id FROM Users WHERE email = %s', user_register['email']
    )

    response = cursor.fetchone()

    if response is not None:
        print('DEU ERRO')
        error = 'Email {} already registered'.format(user_register['email'])

    if error is None:
        cursor.execute(
            'INSERT INTO Users (name, gender, email, birth_date, password, medicalRegister, userType) VALUES (%s,%s,%s,%s,%s,%s,%s)',
            (user_register['name'], user_register['gender'], user_register['email'], user_register['birth_date'], 
            generate_password_hash(user_register['password']), user_register['medicalRegister'], user_register['userType'])
        )
        db.commit()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    return json.dumps({'success':False}), 300, {'ContentType':'application/json'}
    #flash(error)


@bp.route('/login', methods=(['POST']))
def login():

    user_login = {
        'email' : request.form['email'],
        'password' : request.form['password']
        }

    error = None
    db = g.db
    cursor = g.db.cursor()

    cursor.execute('SELECT * FROM Users WHERE email=%s', (user_login['email']))

    user = cursor.fetchone()

    if user is None:
        error = 'Incorrect email'
    elif not check_password_hash(user['password'], user_login['password']):
        error = 'Incorrect Password'

    if error is None:
        session.clear()
        session['user_id'] = user['id']
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    return json.dumps({'success':False}), 300, {'ContentType':'application/json'}
    #flash(error)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    db = get_db()
    cursor = db.cursor()

 
    if user_id is None:
        print('ALWAYS HERE')
        g.user = None
        return 'NOT LOGGED'
    else:
        cursor.execute('SELECT * FROM Users WHERE id = %s', (user_id,))
        g.user = cursor.fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return 'User not logged in'
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    return wrapped_view