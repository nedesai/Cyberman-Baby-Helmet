from flask import *
from extensions import connect_to_database

model = Blueprint('model', __name__, template_folder='templates')

#-----------#
# Model API #
#-----------#
@model.route('/api/v1/model', methods=['GET', 'POST', 'DELETE'])
def model_route():
    db = connect_to_database()

    #----------------#
    # Error-checking #
    #----------------#
    json_data = request.get_json()

    # Check for missing keys in the JSON request
    if data_missing_keys(json_data, ['username, patientid']):
        error = 'Error: request missing required keys (username, patientid)'
        return jsonify(error=error_message), 422

    # Check that user has access to this patient
    cur = db.cursor()
    cur.execute('SELECT * FROM UserPatientLink WHERE username=\'' + username + '\' AND patientid=' + patientid)
    if len(cur.fetchall() == 0):
        error = 'Error: User does not have permission to access this patient\'s models'
        return jsonify(error=error), 403

    #--------------#
    # GET requests #
    #--------------#
    if request.method == 'GET':
        check_errors()

        #-------------------#
        # Return model info #
        #-------------------#
        cur = db.cursor()
        cur.execute('SELECT url, description FROM Model WHERE patientid=' + str(patientid))
        models = []
        for m in cur.fetchall():
            models.append( { url: m['url'], description: m['description'] } )

        return jsonify(models=models), 200

    #-----------------#
    # DELETE requests #
    #-----------------#
    if request.method == 'DELETE':
        return jsonify({}), 200

#-----------#
# Utilities #
#-----------#
def data_missing_keys(json_data, required_keys):
    missing_keys = False
    for key in required_keys():
        if key not in json_data:
            missing_keys = True
    return missing_keys