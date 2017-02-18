from flask import *
from extensions import connect_to_database

model = Blueprint('model', __name__, template_folder='templates')

#-------------#
# model API #
#-------------#
@model.route('/api/v1/model', methods=['GET', 'POST', 'DELETE'])
def model_route():
	db = connect_to_database()
	json_data = request.get_json()

	if data_missing_keys(json_data, ['']):
		return 422

	cur = db.cursor()
	cur.execute('SELECT ')

    return render_template('index.html')

def data_missing_keys(json_data, required_keys):
	missing_keys = False
	for key in required_keys():
		if key not in json_data:
			missing_keys = True
	return missing_keys