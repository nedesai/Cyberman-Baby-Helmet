from flask import *

logout = Blueprint('logout', __name__, template_folder='templates')

@logout.route('/api/v1/logout', methods=['POST'])
def logout_route():
	if 'username' in session:
		session.clear()
		return jsonify(status="OK"), 204
	else:
		return jsonify(error="You do not have the necessary credentials for the resource"), 401