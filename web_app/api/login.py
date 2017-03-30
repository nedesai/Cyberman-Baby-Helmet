from flask import *
from flask import session
from extensions import connect_to_database
from datetime import datetime
from .api_utilities import data_missing_keys, check_user_permissions, NO_ERRORS
import os
import hashlib
import uuid
import re

login = Blueprint('login', __name__, template_folder='templates')

@login.route('/api/v1/login', methods=['GET', 'POST'])
def login_route():
	print ("debug")
	db = connect_to_database()
	cur = db.cursor()
	name = False
	if 'username' in session:
		user = session['username']
		cur.execute('''Select firstname, lastname from User where username = ''' + "'" + user + "'")
		name = cur.fetchall()

	if request.method == 'GET':
		name = False
		if 'username' in session:
			user = session['username']
			cur.execute('''Select firstname, lastname from User where username = ''' + "'" + user + "'")
			name = cur.fetchall()
		option = [
			"user_not_found",
			"pass_not_found",
			name
		]
		
		options = { "error" : option }
		return jsonify(error=options)
	if request.method == 'POST':
		print ("hello")
		found_user = True
		found_pass = True
		user_input = request.form['username']
		user_input = user_input.lower()
		pass_input = request.form['password']
		
		print (pass_input + " " + user_input)

		cur = db.cursor()
		name = False
		if 'username' in session:
			user = session['username']
			cur.execute('''Select firstname, lastname from User where username = ''' + "'" + user + "'")
			name = cur.fetchall()
		cur.execute('''Select username, password FROM User where username = ''' + "'" + user_input + "'")
		msgs = cur.fetchall()

		if not msgs:
			return 404

		split_pass = msgs[0][1].split('$', 2)
		
		print (split_pass)

		#algorithm = 'sha512'
		#salt = split_pass[1]
		#m = hashlib.new(algorithm)
		#m.update(salt + pass_input)
		#password_hash = m.hexdigest()

		if not msgs:
			print ("no msgs return bad")
			found_user = False
		else:
			split_pass = msgs[0][1].split('$', 2)
			print (split_pass[2] + " " + pass_input)
			if split_pass[2] != pass_input:
				found_pass = False
		if found_user == False or found_pass == False:
			option = [
				"user_not_found " + str(found_user),
				"pass_not_found " + str(found_pass),
				name
			]
			
			options = { "error" : option }
			return jsonify(error=options)	
		else:
			name = False
			session['username'] = user_input
			if 'username' in session:
				user = session['username']
				cur.execute('''Select firstname, lastname from User where username = ''' + "'" + user + "'")
				name = cur.fetchall()
			#render page that the user came from
			
			option = [
				"user_not_found",
				"pass_not_found",
				name
			]
			options = { "error" : option }
			return jsonify(error=options)

