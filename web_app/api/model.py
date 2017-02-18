from flask import *
from extensions import connect_to_database

model = Blueprint('model', __name__, template_folder='templates')

#-------------#
# model API #
#-------------#
@model.route('/api/v1/model', methods=['GET', 'POST', 'DELETE'])
def model_route():
    return render_template('index.html')