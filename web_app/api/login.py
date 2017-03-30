from flask import *
from flask import session
import os
import hashlib
import uuid
import re

login = Blueprint('login', __name__, template_folder='templates')

def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
            url_for(default)

@login.route('/api/v1/login', methods=['GET', 'POST'])
def login_route():
	cur = mysql.connection.cursor()
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
		options = [
			"user_not_found",
			"pass_not_found",
			name
		]
		return render_template("index.html", **options)
	if request.method == 'POST':
		found_user = True
		found_pass = True
		user_input = request.form['username']
		user_input = user_input.lower()
		pass_input = request.form['password']

		cur = mysql.connection.cursor()
		name = False
		if 'username' in session:
			user = session['username']
			cur.execute('''Select firstname, lastname from User where username = ''' + "'" + user + "'")
			name = cur.fetchall()
		cur.execute('''Select username, password FROM User where username = ''' + "'" + user_input + "'")
		msgs = cur.fetchall()

		if not msgs:
			return render_template("index.html", user_not_found = False, pass_not_found = True)

		split_pass = msgs[0][1].split('$', 2)

		algorithm = 'sha512'
		salt = split_pass[1]
		m = hashlib.new(algorithm)
		m.update(salt + pass_input)
		password_hash = m.hexdigest()

		if not msgs:
			found_user = False
		else:
			split_pass = msgs[0][1].split('$', 2)
			if split_pass[2] != password_hash:
				found_pass = False
		if found_user == False or found_pass == False:
			options = [
				"user_not_found " + str(found_user),
				"pass_not_found " + str(found_pass),
				name
			]
			return render_template("index.html", **options)	
		else:
			name = False
			session['username'] = user_input
			if 'username' in session:
				user = session['username']
				cur.execute('''Select firstname, lastname from User where username = ''' + "'" + user + "'")
				name = cur.fetchall()
			#render page that the user came from
			
			options = [
				"user_not_found",
				"pass_not_found",
				name
			]
			return redirect(url_for('patients.patient_route'))

