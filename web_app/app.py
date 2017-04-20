from flask import Flask, render_template
import extensions
import photo_email_service
import config
import api
import controllers

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

# Register the APIs
app.register_blueprint(api.patient)
app.register_blueprint(api.photos)
app.register_blueprint(api.model)
app.register_blueprint(api.login)
app.register_blueprint(api.logout)
app.register_blueprint(api.register)
app.register_blueprint(controllers.main)

# Secret key for sessions & cookies
app.secret_key = '4fd75asf_a8d4f_sad84f84'

# Listen on external IPs
if __name__ == '__main__':
    # Starts the photo email service as a separate thread
    pes = photo_email_service.PhotoEmailService()
    pes.start_listening()

    # Listens on external IPs
    app.run(host=config.env['host'], port=config.env['port'], debug=True)
