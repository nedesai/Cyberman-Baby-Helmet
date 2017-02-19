from flask import *
from extensions import connect_to_database
from datetime import datetime
# import boto3
import hashlib

model = Blueprint('model', __name__, template_folder='templates')

NO_ERRORS = "NO_ERRORS"

#-----------#
# Model API #
#-----------#
@model.route('/api/v1/model', methods=['GET', 'POST', 'DELETE'])
def model_route():
    db = connect_to_database()

    #---------------------------------------------#
    # Error-checking for DELETE and POST requests #
    #---------------------------------------------#
    if request.method == 'DELETE' or request.method == 'POST':
        json_data = request.get_json()

        # Check for missing keys
        required_keys = ['username', 'patientid']
        if request.method == 'DELETE':
            missing_keys.append('modelid')
        if data_missing_keys(json_data, missing_keys):
            error = 'Error: request missing required keys'
            return jsonify(error=error), 422

        # Check if the user has permission to access this patient's data
        error, status_code = check_user_permissions(db, username, json_data['patientid'])
        if error != NO_ERRORS:
            return jsonify(error=error), status_code

    #--------------#
    # GET requests #
    #--------------#
    if request.method == 'GET':
        username = request.args.get('username')
        patientid = request.args.get('patientid')

        #----------------#
        # Error-checking #
        #----------------#
        # Check for missing query parameters
        if username == None or patientid == None:
            error = 'Error: request missing required query parameters'
            return jsonify(error=error), 422

        # Check if the user has permission to access this patient's data
        error, status_code = check_user_permissions(db, username, patientid)
        if error != NO_ERRORS:
            return jsonify(error=error), status_code

        #-----------------------#
        # Get model information #
        #-----------------------#
        cur = db.cursor()
        cur.execute('SELECT url, description FROM Model WHERE patientid=' + patientid)
        models = []
        for m in cur.fetchall():
            models.append( { url: m['url'], description: m['description'] } )

        return jsonify(models=models), 200

    #---------------#
    # POST requests #
    #---------------#
    elif request.method == "POST":
        check_errors()

        model_description = request.form['description']
        username = json_data['username']
        patientid = json_data['patientID']
        model_file = request.files['file']
        current_date_time = datetime.now()

        hash_url = hashlib.sha512(str.encode(patientid + current_date_time))

        '''
        s3_client = boto3.client('s3')
        s3_client.upload_file(model_file, 'babyhead', model_file)
        '''

        cur = db.cursor()
        sql_string = 'INSERT INTO Model (filename, description, uploaddate)'
        sql_string += 'VALUES (\'' + hash_url + '\', \'' +  model_description + '\', \'' + current_date_time + '\')'
        sql_string += 'WHERE patientid=\'patientid\''
        cur.execute(sql_string)

        return 200

    #-----------------#
    # DELETE requests #
    #-----------------#
    elif request.method == 'DELETE':
        cur = db.cursor()
        cur.execute('DELETE FROM Model WHERE modelid=' + json_data['modelid'])
        return 200

#-----------#
# Utilities #
#-----------#
def data_missing_keys(json_data, required_keys):
    missing_keys = False
    for key in required_keys:
        if key not in json_data:
            print(key)
            missing_keys = True
    return missing_keys

def check_user_permissions(db, username, patient):
    error = NO_ERRORS
    cur = db.cursor()
    cur.execute('SELECT * FROM UserPatientLink WHERE username=\'' + username+ '\' AND patientid=' + patient)
    if len(cur.fetchall()) == 0:
        error = 'Error: User does not have permission to access this patient\'s models'
    return error, 403