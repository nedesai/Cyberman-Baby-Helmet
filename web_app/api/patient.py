from flask import *
from extensions import connect_to_database

patient = Blueprint('patient', __name__, template_folder='templates')

#-------------#
# Patient API #
#-------------#
@patient.route('/api/v1/patient', methods=['GET', 'POST', 'DELETE'])
def patient_route():
    return render_template('index.html')