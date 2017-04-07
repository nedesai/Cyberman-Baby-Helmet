from flask import *
from extensions import connect_to_database
import hashlib
import uuid

register = Blueprint('register', __name__, template_folder='templates')

#----------------#
# Register route #
#----------------#
@register.route('api/v1/register', methods=['GET', 'POST'])
def register_route():
	db = connect_to_database()

	#---------------#
	# POST requests #
	#---------------#
	if request.method == 'POST':
		user_info = request.get_json()
		username = user_info['username']
		password1 = user_info['password1']
		password2 = user_info['password2']
		firstname = user_info['firstname']
		lastname = user_info['lastname']
		email = user_info['email']

		#---------------------------------------#
		# Check if a valid username was entered #
		#---------------------------------------#
		
		# Check if username already exists
		cur = db.cursor()
		cur.execute('SELECT * FROM User WHERE username=\'{}\''.format(username))
		if len(cur.fetchall()) != 0:
			return jsonify(errors="User already exists"), 400

		# Check if passwords are the same
		elif password1 != password2:
			return jsonify(errors="Passwords don't match")

		else:
			# Insert user into database
			cur = db.cursor()

			algorithm = 'sha512'
			salt = uuid.uuid4().hex
			m = hashlib.new(algorithm)
			m.update(salt + password1)
			password_hash = m.hexdigest()
			password = "$".join([algorithm, salt, password_hash])

			cur.execute('INSERT INTO User (username, password, firstname, lastname, email)' 
						'VALUES ({}, {}, {}, {}, {});'.format(username, password, firstame, lastname, email))