from flask import (
    Blueprint, flash, g, request, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import json
from flask_cors import cross_origin
from flask import Response
import pandas as pd
from joblib import load
import numpy as np

bp = Blueprint('diagnostic', __name__, url_prefix='/diagnostic')

@bp.route('/anthropometric', methods=(['POST']))
@cross_origin(supports_credentials=True)
def post_antropometric():
    
    if request.method == 'POST':
        
        if not request.form:
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

        }


        db = g.db
        cursor = db.cursor()

        
        try:
            cursor.execute("""INSERT INTO Anthropometrics (userId,heartBeats,systolicPressure,diastolicPressure,
                                                            weight,height,bmi,armCircunference,waistCircunference,
                                                            sagittalAbdominalDiameter,fistStrength)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                            (user_antropometrics['userId'],user_antropometrics['heartBeats'],user_antropometrics['systolicPressure'],user_antropometrics['diastolicPressure'],
                            user_antropometrics['weight'],user_antropometrics['height'],user_antropometrics['bmi'],user_antropometrics['armCircunference'],
                            user_antropometrics['waistCircunference'],user_antropometrics['sagittalAbdominalDiameter'],user_antropometrics['fistStrength'])
                            )
            db.commit()
            return json.dumps({'success':True},), 201, {'ContentType':'application/json'}
        except:
            return json.dumps({'success':False}), 500, {'ContentType':'application/json'}


@bp.route('/anthropometric', methods=(['GET']))
@cross_origin(supports_credentials=True)
def get_antropometric():

    userId = session['user_id']
    db = g.db
    cursor = db.cursor()

    cursor.execute('SELECT * FROM Anthropometrics WHERE userId = %s', (userId))

    data = cursor.fetchone()

    return json.dumps({'success':True,'data':data}), 200, {'ContentType':'application/json'}


@bp.route('/personalData', methods=(['POST']))
@cross_origin(supports_credentials=True)
def post_socioeconomics():




    user_personalData = {
        'userId' : session['user_id'],
        'age': request.form['age'],
        'gender': request.form['gender'],
        'educationalLevel' : request.form['educationalLevel'],
        'householdIncome'  : request.form['householdIncome'],
        'totalPeopleResidence' : request.form['totalPeopleResidence']
    }


    db = g.db
    cursor = db.cursor()


    try:
        cursor.execute(
            'SELECT userId FROM PersonalData WHERE userId = %s', user_personalData['userId']
        )
        response = cursor.fetchone()
    except:
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'}


    if response is None:
        try:
            cursor.execute("""INSERT INTO PersonalData (userId, age, educationalLevel, householdIncome, totalPeopleResidence, gender )
                            VALUES (%s,%s,%s,%s,%s,%s)""", 
                            (user_personalData['userId'],
                            user_personalData['age'],
                            user_personalData['educationalLevel'], 
                            user_personalData['householdIncome'],
                            user_personalData['totalPeopleResidence'],
                            user_personalData['gender'],                                         
                            )
                            )
            db.commit()
            data = {
                'message':"Personal data inserted successfully"
            }
            js = json.dumps(data)
            resp = Response(js, status=200, mimetype='application/json')
            return resp
        except:
            data = {
                'message':"Failed on inserting personal data"
            }
            js = json.dumps(data)
            resp = Response(js, status=500, mimetype='application/json')
            return resp

    else:
        try:
            cursor.execute("""UPDATE PersonalData
                                SET
                                age = %s, 
                                educationalLevel = %s, 
                                householdIncome = %s, 
                                totalPeopleResidence = %s, 
                                gender = %s 
                                WHERE userId = %s;""", 
                    (
                    user_personalData['age'],
                    user_personalData['educationalLevel'], 
                    user_personalData['householdIncome'],
                    user_personalData['totalPeopleResidence'],
                    user_personalData['gender'], 
                    user_personalData['userId']                                                       
                    )
                    )
            db.commit()  

            data = {
                'message':"Personal data updated successfully"
            }
            js = json.dumps(data)
            resp = Response(js, status=200, mimetype='application/json')
            return resp
        except Exception as e:
            print(e)
            data = {
                'message':"Failed on updating personal data"
            }
            v
            return resp


@bp.route('/nutrients', methods=(['POST']))
@cross_origin(supports_credentials=True)
def post_nutrients():

    user_nutrients = {
    'userId': session['user_id'],                 
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

    try:
        db = g.db
        cursor = db.cursor()
    except:
        data = {
            'message':"Server Error"
        }
        js = json.dumps(data)
        print('ERROR WHILE GETTING DATABASE')
        resp = Response(js, status=500, mimetype='application/json')
        return resp

    try:
        cursor.execute(
            'SELECT userId FROM Nutrients WHERE userId = %s', user_nutrients['userId']
        )
        response = cursor.fetchone()
    except Exception as e:
        print(e)
        print('ERROR WHILE GETTING USER FROM DATABASE')
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'}

    if response is None:
        try:
            cursor.execute(
                """
                        INSERT INTO Nutrients (userId, calories, proteins, carbohydrates, 
                                        totalSugar, fibers, fats, saturatedFat, monounsaturatedFat,
                                        polyunsaturatedFat, cholesterol, alcohol)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    user_nutrients['userId'],
                    user_nutrients['calories'],
                    user_nutrients['proteins'],
                    user_nutrients['carbohydrates'],
                    user_nutrients['totalSugar'],
                    user_nutrients['fibers'],
                    user_nutrients['fats'],
                    user_nutrients['saturatedFat'],
                    user_nutrients['monounsaturatedFat'],
                    user_nutrients['polyunsaturatedFat'],
                    user_nutrients['cholesterol'],
                    user_nutrients['alcohol']
                )
            )

            print('INSERTING USER DATA (NUTRIENTS)')
            db.commit()
            data = {
                'message':"Nutrients data updated successfully"
            }
            js = json.dumps(data)
            resp = Response(js, status=200, mimetype='application/json')
            return resp
        except:
            data = {
                'message':"Failed on inserting nutrients data"
            }
            js = json.dumps(data)
            resp = Response(js, status=500, mimetype='application/json')
            return resp
    else:
        try:
            print("IM HERE")
            cursor.execute(
                """
                UPDATE Nutrients SET
                                    calories = %s,
                                    proteins = %s,
                                    carbohydrates = %s, 
                                    totalSugar = %s, 
                                    fibers = %s, 
                                    fats = %s, 
                                    saturatedFat = %s, 
                                    monounsaturatedFat = %s,
                                    polyunsaturatedFat = %s, 
                                    cholesterol = %s, 
                                    alcohol = %s
                WHERE userId = %s
                """,
                (
                    user_nutrients['calories'],
                    user_nutrients['proteins'],
                    user_nutrients['carbohydrates'],
                    user_nutrients['totalSugar'],
                    user_nutrients['fibers'],
                    user_nutrients['fats'],
                    user_nutrients['saturatedFat'],
                    user_nutrients['monounsaturatedFat'],
                    user_nutrients['polyunsaturatedFat'],
                    user_nutrients['cholesterol'],
                    user_nutrients['alcohol'],
                    user_nutrients['userId']                    
                )
            )

            print('UPDATING USER DATA (NUTRIENTS)')

            db.commit()
            data = {
                'message':"Nutrients data updated successfully"
            }
            js = json.dumps(data)
            resp = Response(js, status=200, mimetype='application/json')
            return resp
        except:
            data = {
                'message':"Failed on updating nutrients data"
            }
            js = json.dumps(data)
            resp = Response(js, status=500, mimetype='application/json')
            return resp



@bp.route('/socioeconomics', methods=(['GET']))
@cross_origin(supports_credentials=True)
def get_socioeconomics():

    userId = session['user_id']
    db = g.db
    cursor = db.cursor()

    cursor.execute('SELECT * FROM Socioeconomics WHERE userId = %s', (userId))

    data = cursor.fetchone()

    return json.dumps({'success':True,'data':data}), 200, {'ContentType':'application/json'}


@bp.route('/makeDiagnostic', methods=(['GET']))
@cross_origin(supports_credentials=True)
def makeDiagnostic():

    userId = session['user_id']

    db = g.db
    cursor = db.cursor()

    cursor.execute("""SELECT
                        A.heartBeats as Batimentos,
                        A.heartBeats as BatimentosRegulares,
                        A.systolicPressure as MediaPressaoSistolica,
                        A.diastolicPressure as MediaPressaoDiastolica,
                        A.weight as Peso,
                        A.height as AlturaEmPe,
                        A.bmi as IMC,
                        A.armCircunference as CircunferenciaDoBraco,
                        A.waistCircunference as CircunferenciaDaCintura,
                        A.sagittalAbdominalDiameter as DiametroAbdominalSagital,
                        A.fistStrength as ForcaNoPunho,
                        DATEDIFF(yy, U.birth_date, getdate()) as Idade,
                        U.gender as Genero,
                        P.educationalLevel as GrauDeEscolaridade,
                        P.totalPeopleResidence as TotalPessoasResidencia ,
                        P.householdIncome as RendimentoFamiliarTotal,
                        N.calories as Calorias,
                        N.proteins as Proteinas,
                        N.carbohydrates as Carboidratos,
                        N.totalSugar as AcucarTotal,
                        N.fibers as Fibras,
                        N.fats as Gorduras,
                        N.saturatedFat as GorduraSaturada,
                        N.monounsaturatedFat as GorduraMonosaturada,
                        N.polyunsaturatedFat as GorduraPoliinsaturada,
                        N.cholesterol as Colesterol,
                        N.alcohol as Alcool,
                        A.PAL as NivelAtividadeFisica
                    FROM Anthropometrics A
                    JOIN Users U ON A.userId = U.id
                    JOIN PersonalData P ON P.userId = U.id
                    JOIN Nutrients N ON N.userId = U.id
                    WHERE U.id = %s;""", (userId))

    data = cursor.fetchone()

    patient = pd.DataFrame.from_dict(data, orient='index');

    print(patient)

    # Calling Diagnostic Function
    result = diagnostic(patient)

    data = {
        'isDiabetic': result
    }
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


"""age,calories,proteins,
    carbohydrates,totalSugar,fibers,fats,saturatedFat,monounsaturatedFat,
    polyunsaturatedFat,cholesterol,alcohol)
"""

def diagnostic(patient):
    bagging = load('flaskr/decision_tree.joblib')
    result = bagging.predict(np.array(patient).reshape(1,-1))[0]
    print(f'RESULTADO: {bool(result)}')
    return bool(result)
