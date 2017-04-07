from flask import *
from flask import session
from extensions import connect_to_database
from .api_utilities import data_missing_keys, check_user_permissions, NO_ERRORS
import MySQLdb
import MySQLdb.cursors
import hashlib
import uuid


login = Blueprint('login', __name__, template_folder='templates')

@login.route('/api/v1/login', methods=['GET', 'POST'])

def login_route():
  if request.method == 'GET':
    if 'username' in session:
      return jsonify(username=session['username'])
    else:
      return jsonify(username='')
  if request.method == 'POST':
    session.clear()
    if 'username' in session:
      redirect(url_for('main.main_route'))
    else:
      posteddata = request.get_json()
      if 'username' not in posteddata or 'password' not in posteddata:
        return jsonify(error="You did not provide the necessary fields"), 422
      db = connect_to_database()
      cur = db.cursor()
      cur.execute("SELECT firstname, lastname, password FROM User WHERE username='" + posteddata['username'] + "'")
      #Check for valid username
      if cur.rowcount != 0:
        results = cur.fetchall()
        session['username'] = posteddata['username']
        session['logged_in'] = True
        results = results[0]
        session['firstname'] = results['firstname']
        session['lastname'] = results['lastname']
        jsonobj = {'username': posteddata['username']}

        #Check for correct password
        password_table = results['password']
        
        sep = password_table.find("$")
        sep2 = password_table.rfind("$")

        hash_alg = password_table[0:sep]
        salt = password_table[sep + 1: sep2]
        m = hashlib.new(hash_alg)
        m.update(salt + posteddata['password'])
        password_hash = m.hexdigest()
        password_check = hash_alg + "$" + salt + "$" + password_hash
        if password_table != password_check:
          session.clear()
          return jsonify(error="Password is incorrect for the specified username"), 422
        return jsonify(jsonobj), 200
      else:
        return jsonify(error="Username does not exist"), 404
