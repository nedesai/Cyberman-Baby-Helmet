from flask import Flask, render_template
import extensions
import controllers
import config
import api

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

# Register the APIs
app.register_blueprint(api.patient)
app.register_blueprint(api.model)

# Secret key for sessions & cookies
app.secret_key = '4fd75asf_a8d4f_sad84f84'

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host=config.env['host'], port=config.env['port'], debug=True)
