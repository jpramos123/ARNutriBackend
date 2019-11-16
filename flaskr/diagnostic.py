from flask import (
    Blueprint, flash, g, request, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import json

bp = Blueprint('diagnostic', __name__, url_prefix='/diagnostic')

@bp.route('/anthropometric', methods=(['POST']))
def post_antropometric():

    if request.method == 'POST':

        if not request.form or 'userId' not in request.form.keys():
            abort(400)
        
        user_antropometrics = {
            'userId': session['user_id'],
            'heartBeats' : request.form['heartBeats'],
            'systolicPressure': request.form['systolicPressure'],
            'diastolicPressure': request.form['diastolicPressure'],     
            'weight': request.form['weight'], 
            'height': request.form['height'], 
            'bmi': request.form['bmi'],
            'armCircunference': request.form['armCircunference'], 
            'waistCircunference': request.form['waistCircunference'], 
            'sagittalAbdominalDiameter': request.form['sagittalAbdominalDiameter'], 
            'fistStrength': request.form['fistStrength'],
            'age': request.form['age'],                  
            'calories': request.form['calories'],                  
            'proteins': request.form['proteins'],                  
            'carbohydrates': request.form['carbohydrates'],                  
            'totalSugar': request.form['totalSugar'],                  
            'fibers': request.form['fibers'],                  
            'fats': request.form['fats'],                  
            'saturatedFat': request.form['saturatedFat'],                  
            'monounsaturatedFat': request.form['monounsaturatedFat'],                  
            'polyunsaturatedFat': request.form['polyunsaturatedFat'],                  
            'cholesterol': request.form['cholesterol'],                  
            'alcohol': request.form['alcohol'],
        }

        db = g.db
        cursor = db.cursor()

        
        try:
            cursor.execute("""INSERT INTO Anthropometrics (userId,heartBeats,systolicPressure,diastolicPressure,
                                                            weight,height,bmi,armCircunference,waistCircunference,
                                                            sagittalAbdominalDiameter,fistStrength,age,calories,proteins,
                                                            carbohydrates,totalSugar,fibers,fats,saturatedFat,monounsaturatedFat,
                                                            polyunsaturatedFat,cholesterol,alcohol)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                            (user_antropometrics['userId'],user_antropometrics['heartBeats'],user_antropometrics['systolicPressure'],user_antropometrics['diastolicPressure'],
                            user_antropometrics['weight'],user_antropometrics['height'],user_antropometrics['bmi'],user_antropometrics['armCircunference'],
                            user_antropometrics['waistCircunference'],user_antropometrics['sagittalAbdominalDiameter'],user_antropometrics['fistStrength'],user_antropometrics['age'],
                            user_antropometrics['calories'],user_antropometrics['proteins'],user_antropometrics['carbohydrates'],user_antropometrics['totalSugar'],user_antropometrics['fibers'],
                            user_antropometrics['fats'],user_antropometrics['saturatedFat'],user_antropometrics['monounsaturatedFat'],user_antropometrics['polyunsaturatedFat'],
                            user_antropometrics['cholesterol'],user_antropometrics['alcohol'])
                            )
            db.commit()
            return json.dumps({'success':True},), 201, {'ContentType':'application/json'}
        except:
            return json.dumps({'success':False}), 500, {'ContentType':'application/json'}


@bp.route('/anthropometric', methods=(['GET']))
def get_antropometric():

    userId = session['user_id']
    db = g.db
    cursor = db.cursor()

    cursor.execute('SELECT * FROM Anthropometrics WHERE userId = %s', (userId))

    data = cursor.fetchone()

    return json.dumps({'success':True,'data':data}), 200, {'ContentType':'application/json'}


@bp.route('/socioeconomics', methods=(['POST']))
def post_socioeconomics():

    user_socioeconomics = {
        'userId' : session['user_id'],
        'educationalLevel' : request.form['educationalLevel'],
        'householdIncome'  : request.form['householdIncome'],
    }

    db = g.db
    cursor = db.cursor()

    try:
        cursor.execute("""INSERT INTO Socioeconomics (userId, educationalLevel, householdIncome)
                          VALUES (%s,%s,%s)""", (user_socioeconomics['userId'], user_socioeconomics['educationalLevel'], user_socioeconomics['householdIncome'])
                          )
        db.commit()
        
        return json.dumps({'success':True},), 201, {'ContentType':'application/json'}

    except:
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'}


@bp.route('/socioeconomics', methods=(['GET']))
def get_socioeconomics():

    userId = session['user_id']
    db = g.db
    cursor = db.cursor()

    cursor.execute('SELECT * FROM Socioeconomics WHERE userId = %s', (userId))

    data = cursor.fetchone()

    return json.dumps({'success':True,'data':data}), 200, {'ContentType':'application/json'}


@bp.route('/makeDiagnostic', methods=(['GET']))
def makeDiagnostic():

    userId = session['user_id']

    db = g.db
    cursor = db.cursor()

    cursor.execute("""SELECT heartBeats, systolicPressure, diastolicPressure
	   weight, height, bmi, armCircunference, waistCircunference,
	   sagittalAbdominalDiameter, fistStrength, age, calories,
	   proteins, carbohydrates, totalSugar, fibers, fats, saturatedFat,
	   monounsaturatedFat, polyunsaturatedFat, cholesterol, alcohol, s.educationalLevel, s.householdIncome FROM Anthropometrics a
RIGHT JOIN Socioeconomics s ON s.userId = a.userId
WHERE a.userId = %s;""", (userId))

    data = cursor.fetchone()

    

    return 'OI'