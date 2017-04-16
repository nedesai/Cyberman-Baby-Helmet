from flask import *
from extensions import connect_to_database
import hashlib
import uuid

register = Blueprint('register', __name__, template_folder='templates')

def session_exists():
	if username in session:
		return True
	else:
		return False

#----------------#
# Register route #
#----------------#
@register.route('/api/v1/register', methods=['GET', 'POST', 'PUT'])
def register_route():
	db = connect_to_database()

	#---------------#
	# POST requests #
	#---------------#
	if request.method == 'POST':
		user_info = request.get_json()
		username = str(user_info['username'])
		password1 = str(user_info['password1'])
		password2 = str(user_info['password2'])
		firstname = str(user_info['firstname'])
		lastname = str(user_info['lastname'])
		email = str(user_info['email'])

		#---------------------------------------#
		# Check if a valid username was entered #
		#---------------------------------------#
		
		# Check if username already exists
		cur = db.cursor()
		cur.execute('SELECT * FROM User WHERE username=\'{}\''.format(username))
		if len(cur.fetchall()) != 0:
			return jsonify(errors=["User already exists"]), 400

		# Check if passwords are the same
		elif password1 != password2:
			return jsonify(errors=["Passwords don't match"]), 400

		else:
			# Insert user into database
			cur = db.cursor()

			algorithm = 'sha512'
			salt = uuid.uuid4().hex
			m = hashlib.new(algorithm)
			m.update(salt + password1)
			password_hash = m.hexdigest()
			password = str("$".join([algorithm, salt, password_hash]))

			cur.execute("INSERT INTO User (username, password, firstname, lastname, email) VALUES ('" + username + "', '" + password + "', '" + firstname + "', '" + lastname + "', '" + email + "');")
			return jsonify(status="OK"), 202

	#----------------#
	# PUT: Edit User #
	#----------------#
	elif request.method == 'PUT':
		json_data = request.get_json()
		success = {
			"updated": [],
			"messages": []
		}
		error_messages = []
		login_errors = False
		#----------------#
		# Error checking #
		#----------------#
		# Return with an error message and 401 if user is not logged in
		if not session:
			error_messages.append("You are not logged in")
			return jsonify(errors=error_messages), 401

		# Check if username is in session or password length long enough
		if (json_data['username'] != session['username']) or (len(str(json_data['password'])) < 8):
			login_errors = True

		# Check if password entered for user is correct before updating
		cur = db.cursor()
		cur.execute("Select * from User where username = '" + str(json_data['username']) + "';")

		if cur.rowcount == 0:
			login_errors = True

		password = json_data['password']

		output = cur.fetchall()[0]
		password_table = output['password']

		sep      = password_table.find("$")
		sep2     = password_table.rfind("$")
		hash_alg = password_table[0:sep]
		salt     = password_table[sep+1:sep2]

		m = hashlib.new(hash_alg)
		m.update(salt + password)
		password_hash = m.hexdigest()
		password_check = "$".join([hash_alg, salt, password_hash])

		if password_check != password_table:
			login_errors = True

		if login_errors:
			error_messages.append("User credentials incorrect")
			return jsonify(errors=error_messages), 401

		# Handle request
		username	= json_data['username']
		password  = json_data['password']
		firstname	= json_data['firstname']
		lastname	= json_data['lastname']
		password1	= json_data['password1']
		password2	= json_data['password2']
		email     = json_data['email']

		# Check input errors


		updated_password = ""

		if len(password1) != 0 or len(password2) != 0:
			if (len(password1) < 8) or (len(password2) < 8) or (password1 != password2):
				error_messages.append("Could not update. Passwords need to match and be at least 8 characters.")
				return jsonify(errors=error_messages), 403
			else:
				m2 = hashlib.new(hash_alg)
				m2.update(salt + password1)
				updated_password_hash = m2.hexdigest()
				updated_password = "$".join([hash_alg, salt, updated_password_hash])
				if(updated_password == password_table):
					success['messages'].append("New password same as the previous one")

		#check_errors(error_messages, db, check_passwords_flag, check_username_flag, username, firstname, lastname, password1, password2, email)

		#------------------#
		# Update user info #
		#------------------#

		# If the user provided empty values for non-password fields, we just set these
		# variables to the current values for the user.
		# This simplifies the following database insertion.
		if firstname == "":
			firstname = output['firstname']
		else:
			success['updated'].append("Firstname")

		if lastname == "":
			lastname = output['lastname']
		else:
			success['updated'].append("Lastname")

		if email == "":
			email = output['email']
		else:
			success['updated'].append("Email")

		if updated_password == "" and (not len(success['messages'])):
			updated_password = password_table
		else:
			success['updated'].append("Password")

		# Prepare to update User record; username should never be updated
		update_str = "firstname = '" + firstname + "', "
		update_str += "lastname = '" + lastname + "', "
		update_str += "email = '" + email + "', "
		update_str += "password = '" + updated_password + "'"

		# Update User record.
		cur = db.cursor()
		cur.execute("UPDATE User SET " + update_str + " WHERE username = '" + username + "';")

		# Return same JSON response that was sent here, along with an HTTP 201
		return jsonify(success), 201


def check_errors(error_messages, db, check_passwords_flag, check_username_flag, username, firstname, lastname, password1, password2, email):
    # Print '<field> must be no longer than <max_length> characters'
    # if any of these fields exceed <max_length> characters
    check_max_length(error_messages, firstname, 'Firstname', 40)
    check_max_length(error_messages, lastname, 'Lastname', 40)
    check_max_length(error_messages, email, 'Email', 40)

    # Check for syntactically correct email address
    check_email(error_messages, email)

    if check_passwords_flag:
        # Print '<field>s must be at least <min_length> characters long' if
        # any of these fields are less than <min_length> characters.
        check_min_length(error_messages, password1, 'Passwords', 8)

        # Print '<field>s may only contain letters, digits, and underscores'
        # if <field> contains a character that is not a letter nor digit nor underscore
        check_characters(error_messages, password1, "Passwords")

        # Check that password1 has at least 1 character and 1 number,
        # and that password1 == password2
        check_passwords(error_messages, password1, password2)
    
    if check_username_flag:
        # Print '<field>s must be at least <min_length> characters long' if
        # any of these fields are less than <min_length> characters.
        check_min_length(error_messages, username, 'Usernames', 3)

        # Print '<field> must be no longer than <max_length> characters'
        # if any of these fields exceed <max_length> characters
        check_max_length(error_messages, username, 'Username', 40)

        # Print '<field>s may only contain letters, digits, and underscores'
        # if <field> contains a character that is not a letter nor digit nor underscore
        check_characters(error_messages, username, "Usernames")

        # Check to see if username is already taken
        cur = db.cursor()
        cur.execute('SELECT username FROM User')
        results = cur.fetchall()
        for result in results:
            if username == result['username']:
                error_messages.append("This username is taken")
                break
