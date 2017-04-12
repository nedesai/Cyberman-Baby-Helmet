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
			return jsonify(errors="User already exists"), 400

		# Check if passwords are the same
		elif password1 != password2:
			return jsonify(errors="Passwords don't match"), 400

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
		#----------------#
		# Error checking #
		#----------------#
		# Return with an error message and 401 if user is not logged in
		if not session_exists():
			append_credentials_error(error_messages)
			return jsonified_errors(error_messages), 401

		# Check for missing keys; return with error and a 422 immediately if key is missing
		if missing_key(json_data):
			append_fields_error(error_messages)
			return jsonified_errors(error_messages, 422)

		# Return with an error message and 403 if logged in user is trying to edit another user
		if json_data['username'] != session['username']:
			append_permissions_error(error_messages)
			return jsonified_errors(error_messages, 403)

		username	= json_data['username']
		firstname	= json_data['firstname']
		lastname	= json_data['lastname']
		password1	= json_data['password1']
		password2	= json_data['password2']
		email		= json_data['email']

		# Do not perform validation on passwords if both are not empty.
		# Never perform username testing
		check_username_flag = False
		check_passwords_flag = True
		if both_passwords_blank(password1, password2):
			check_passwords_flag = False

		check_errors(error_messages, db, check_passwords_flag, check_username_flag, username, firstname, lastname, password1, password2, email)

		#------------------#
		# Update user info #
		#------------------#
		if no_errors(error_messages):
			# If the user provided empty values for non-password fields, we just set these
			# variables to the current values for the user.
			# This simplifies the following database insertion.
			cur = db.cursor()
			cur.execute('SELECT * FROM User WHERE username=\'{}\''.format(username))
			current_user_data = cur.fetchall()[0]
			if firstname == '':
				firstname = current_user_data['firstname']
			elif lastname == '':
				lastname = current_user_data['lastname']
			elif email == '':
				email = current_user_data['email']

			# Prepare to update User record; username should never be updated
			update_str = 'firstname=\'' + firstname + '\', '
			update_str += 'lastname=\'' + lastname + '\', '
			update_str += 'email=\'' + email + '\''

			# Password isn't updated if it was left blank
			if not both_passwords_blank(password1, password2):
				# Encrypt password
				salt = uuid.uuid4().hex
				encrypted_password = encrypt(password1, salt)

				# Add encrypted password to update command
				update_str += ', ' + 'password=\'' + encrypted_password + '\''

			print(update_str) # For debugging the insertion string

			# Update User record.
			cur = db.cursor()
			cur.execute('UPDATE User SET ' + update_str + ' WHERE username=\'' + username + '\'')

			# Update session info
			session['firstname']    =   firstname
			session['lastname']     =   lastname

			# Return same JSON response that was sent here, along with an HTTP 201
			return jsonify( username    =   username,
							firstname   =   firstname,
							lastname    =   lastname,
							password1   =   password1,
							password2   =   password2,
							email       =   email ), 201

		#-------------------------------------------#
		# Send error messages if we have 422 errors #
		#-------------------------------------------#
		return jsonified_errors(error_messages, 422)

#----------------#
# Error messages #
#----------------#

def append_credentials_error(error_messages):
    error_messages.append('You do not have the necessary credentials for the resource')

def append_fields_error(error_messages):
    error_messages.append('You did not provide the necessary fields')

def append_permissions_error(error_messages):
    error_messages.append('You do not have the necessary permissions for the resource')

def missing_key(json_data):
    if (missing('username', json_data) or missing('firstname', json_data) or
       missing('lastname', json_data) or missing('password1', json_data) or
       missing('password2', json_data) or missing('email', json_data)):
       return True
    else:
        return False

def missing(keyname, json_data):
    if keyname not in json_data:
        return True
    else:
        return False

def both_passwords_blank(password1, password2):
    if blank(password1) and blank(password2):
        return True
    else:
        return False

def jsonified_errors(error_messages, error_code):
    error_list_for_json = []
    for e in error_messages:
        error_list_for_json.append({ 'message': e })
    print(error_list_for_json)
    return jsonify(errors=error_list_for_json), error_code

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
