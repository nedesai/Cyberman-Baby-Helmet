from flask import *
from extensions import connect_to_database
from .api_utilities import data_missing_keys, check_user_permissions, NO_ERRORS

patient = Blueprint('patient', __name__, template_folder='templates')

#-------------#
# Patient API #
#-------------#
@patient.route('/api/v1/patient', methods=['GET', 'POST', 'DELETE'])
def patient_route():
    db = connect_to_database()

    #--------------#
    # GET requests #
    #--------------#
    if request.method == "GET":
        username = request.args.get('username')

        #error checking to make sure username exists
        if username == None:
            error = "Error: request missing necessary query parameters"
            return jsonify(error=error), 422

        cur = db.cursor()
        cur.execute('SELECT * FROM Patient WHERE username=\'' + username + '\'')
        patients = []
        for i in cur.fetchall():
            patients.append( {  'patientid': i['patientid'], 
                                'firstname': i['firstname'], 
                                'lastname': i['lastname'], 
                                'dob': str(i['dob']) } )

        return jsonify(patients=patients), 200
    
    #---------------#
    # POST requests #
    #---------------#
    if request.method == 'POST':
        json_data = request.get_json()

        # Check for missing keys
        if data_missing_keys(json_data, ['username', 'firstname', 'lastname', 'dob']):
            error = 'Error: request missing required keys'
            return jsonify(error=error), 422

        # Insert new patient into database
        sql_string = 'INSERT INTO Patient (username, firstname, lastname, dob) VALUES (\''
        sql_string += json_data['username'] + '\', \'' + json_data['firstname'] + '\', \''
        sql_string += json_data['lastname'] + '\', \'' + str(json_data['dob']) + '\')'
        cur = db.cursor()
        cur.execute(sql_string)

        return jsonify({}), 200

    #-----------------#
    # DELETE requests #
    #-----------------#
    elif request.method == 'DELETE':
        json_data = request.get_json()

        # Check for missing keys
        if data_missing_keys(json_data, ['patientid']):
            error = 'Error: request missing required keys'
            return jsonify(error=error), 422

        # Check if the user has permission to delete this patient
        error, status_code = check_user_permissions(db, json_data['username'], json_data['patientid'])
        if error != NO_ERRORS:
            return jsonify(error=error), status_code

        # Delete this patient's models
        cur = db.cursor()
        cur.execute('DELETE FROM Model WHERE patientid=' + json_data['patientid'])

        # Delete this patient
        cur = db.cursor()
        cur.execute('DELETE FROM Patient WHERE patientid=' + json_data['patientid'])
        return jsonify({}), 200