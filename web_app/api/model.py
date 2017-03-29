from flask import *
from extensions import connect_to_database
from datetime import datetime
from .api_utilities import data_missing_keys, check_user_permissions, NO_ERRORS
import boto3
import hashlib

model = Blueprint('model', __name__, template_folder='templates')

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
            required_keys.append('modelid')
        elif request.method == 'POST':
            required_keys.append('filetype, description')
        if data_missing_keys(json_data, required_keys):
            error = 'Error: request missing required keys'
            return jsonify(error=error), 422

        # Check if the user has permission to access this patient's data
        error, status_code = check_user_permissions(db, json_data['username'], json_data['patientid'])
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
            models.append( { 'url': m['url'], 'description': m['description'] } )

        return jsonify(models=models), 200

    #---------------#
    # POST requests #
    #---------------#
    elif request.method == "POST":
        json_data = request.get_json()
        model_description = json_data['description']
        username = json_data['username']
        patientid = json_data['patientid']
        filetype = json_data['filetype']
        model_file = request.files['file']
        current_date_time = datetime.now()

        hash_name = hashlib.sha512(str.encode(patientid + str(current_date_time)))


        #s3_client = boto3.client('s3')
        #s3_client.upload_file(model_file, 'babyhead', model_file)
        #
        #s3_client.upload_file(model_file, 'babyhead', '<name-of-the-file>')
        #url = https://s3.amazonaws.com/babyhead/<name-of-the-file>

        s3_client.upload_file(model_file, 'babyhead', hash_name)
        hash_url = 'https://s3.amazonaws.com/babyhead/hash_name'

        cur = db.cursor()
        sql_string = 'INSERT INTO Model (patientid, filetype, description, url) VALUES (\''
        sql_string += patientid + '\', \'' + filetype + '\', \''
        sql_string += model_description + '\', \'' + str(hash_url) + '\')'
        cur.execute(sql_string)

        return jsonify({}), 200

    #-----------------#
    # DELETE requests #
    #-----------------#
    elif request.method == 'DELETE':
        json_data = request.get_json()
        cur = db.cursor()
        cur.execute('DELETE FROM Model WHERE modelid=' + json_data['modelid'])
        return jsonify({}), 200

