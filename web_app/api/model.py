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
        cur.execute('SELECT url, fbx_url, filename, description, lastmodified FROM Model WHERE patientid=' + patientid)
        models = []
        for m in cur.fetchall():
            models.append( { 'url': m['url'], 'fbx_url': m['fbx_url'], 'filename': m['filename'], 'description': m['description'], 'lastmodified': m['lastmodified'] } )

        return jsonify(models=models), 200

    #---------------#
    # POST requests #
    #---------------#
    elif request.method == "POST":
        json_data = request.get_json()
        model_description = json_data['description']
        username = json_data['username']
        patientid = json_data['patientid']
        model_file = request.files['file']
        current_date_time = datetime.now()

        #hash_url = hashlib.sha512(str.encode(patientid + str(current_date_time)))

        filename, filetype = os.path.splitext(model_file.filename)

        s3_client = boto3.client('s3')
        s3_client.upload_file(model_file, 'babyhead', model_file)
        # s3_client.upload_file(model_file, 'babyhead', '<name-of-the-file>')
        url = 'https://s3.amazonaws.com/babyhead/' + filename



        cur = db.cursor()
        sql_string = 'INSERT INTO Model (patientid, filetype, url, fbx_url, description, filename) VALUES (\''
        sql_string += patientid + '\', \'' + filetype + '\', \''
        sql_string += url + '\', \'' + url + '\', \'' + model_description + '\', \'' + filename '\')'
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

