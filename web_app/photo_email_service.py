from email.mime.text import MIMEText
from extensions import connect_to_database
import threading
import smtplib
import poplib
import email
import time
import os

WEB_APP_EMAIL_USERNAME = 'headmodels481@gmail.com'
WEB_APP_EMAIL_PASSWORD = 'eecs481rules!'

EMAIL_SUBJECT_NO_PHOTOS = 'Email did not contain any photos'
EMAIL_BODY_NO_PHOTOS = '''
It looks like your email didn't contain any photos.

Please try to email us your photos again :)
'''

EMAIL_SUBJECT_INVALID = 'Photos not uploaded to website'
EMAIL_BODY_INVALID = '''
Thank you for sending us your photos that you'd like to convert to a 3D model.

Unfortunately, it looks like your email address is not associated with a registered account.

If this is the case, please create an account on our website.

If you already have an account with us, please try to email your photos from the email address associated with your account.

Happy modeling!
'''

EMAIL_SUBJECT_SUCCESS = 'Photos successfully uploaded to website!'
EMAIL_BODY_SUCCESS = '''
Thank your for submitting your photos.

You can access them on our website.

Happy modeling!
'''

class PhotoEmailService:
	def __init__(self):
		self.db = connect_to_database()

	# Sends an email
	def send_email(self, to_address, subject, body):
		# Build the email message
		msg = MIMEText(body)
		msg['Subject'] = subject
		msg['From'] = WEB_APP_EMAIL_USERNAME
		msg['To'] = to_address

		# Connect to web app's Gmail account and send a response from it.
		# Attempt to send the email 5 times before giving up.
		for x in range(0, 5):
			try:
				s = smtplib.SMTP('smtp.gmail.com', 587) # Port 587
				s.ehlo()
				s.starttls()
				s.ehlo()
				s.login(WEB_APP_EMAIL_USERNAME, WEB_APP_EMAIL_PASSWORD)
				s.send_message(msg)
				s.close()
				break

			except:
				print('Error sending email response! Trying again...')
				time.sleep(2)

	# Returns the email address within the string from_data
	def parse_from_address(self, from_data):
		# For emails sent from Gmail accounts, from_data looks like:
		# Head Model <headmodels481@gmail.com>
		# So, we parse out the email address accordingly
		from_address = ''
		building_from_address = False
		for char in str(from_data):
			if char == '>':
				break
			elif building_from_address:
				from_address += char
			elif char == '<':
				building_from_address = True
		return from_address

	# Parses unread emails and saves the attachments of each email
	# in a folder corresponding to that email
	def save_unread_email_photos(self):
		#----------------------------------------#
		# Connect to our web app's Gmail account #
		#----------------------------------------#
		try:
			connection = poplib.POP3_SSL('pop.gmail.com', 995)
		except:
			print('Error connecting to Gmail. Trying again...')
			return

		# connection.set_debuglevel(1) # Uncomment for verbose debug logs
		connection.user(WEB_APP_EMAIL_USERNAME)
		connection.pass_(WEB_APP_EMAIL_PASSWORD)

		#----------------------------#
		# Get list of raw email data #
		#----------------------------#
		messages = connection.list()
		emails, total_bytes = connection.stat()
		print("{0} new emails received.".format(emails))

		#-----------------------------------#
		# Process emails & save attachments #
		#-----------------------------------#
		for i in range(emails):
			# Get raw message (in bytes) and convert it to a string
			# representation of the message
			response = connection.retr(i+1)
			raw_message = response[1]
			str_message = email.message_from_bytes(b'\n'.join(raw_message))

			#--------------------------------#
			# Check if from address is valid #
			#--------------------------------#
			sender_address = self.parse_from_address(str_message['From'])

			# The photos will be assigned to the user in the database who registered
			# with the email address <sender_address>. If <sender_address> is not in
			# our database, then the user needs to send the email from the address 
			# tied to their account, or register an account with <sender_address>
			# as their email address.
			cur = self.db.cursor()
			cur.execute('SELECT * FROM User WHERE email=\'{0}\''.format(sender_address))
			if len(cur.fetchall()) == 0:
				self.send_email(sender_address,
								EMAIL_SUBJECT_INVALID,
								EMAIL_BODY_INVALID)
				break

			#------------------------------------#
			# Save attachments if email is valid #
			#------------------------------------#
			email_contains_photos = False
			for part in str_message.walk():
				# Skip parts of email that don't contain file attachments
				if (part.get_content_maintype() == 'multipart'
				or part.get('Content-Disposition') is None):
					continue

				filename = part.get_filename()
				if not filename: 
					filename = "test.txt"
				print('Attempting to save the following attachment: {0}'.format(filename))

				self.send_email(sender_address,
								EMAIL_SUBJECT_SUCCESS,
								EMAIL_BODY_SUCCESS)

				# savedir directory needs to exist or else an error will be thrown
				email_contains_photos = True
				savedir="./static/photos/"
				fp = open(os.path.join(savedir, filename), 'wb')
				fp.write(part.get_payload(decode=1))
				fp.close

			# Return an error message via email if the email lacked photos
			if not email_contains_photos:
				self.send_email(sender_address, 
								EMAIL_SUBJECT_NO_PHOTOS, 
								EMAIL_BODY_NO_PHOTOS)

			# Delete email from consideration for processing.
			# Does not actually delete email from Gmail account.
			connection.dele(i+1)

		# Close the connection. This is required to finalize any email deletions.
		connection.quit()

	# Listens for emails indefinitely and saves photos from new emails
	# to the appropriate locations
	def listen_for_emails(self):
		while True:
			time.sleep(2)
			self.save_unread_email_photos()

	def start_listening(self):
		pes_thread = threading.Thread(target=self.listen_for_emails)
		pes_thread.start()

# For testing outside of the web app
if __name__ == '__main__':
	pes = PhotoEmailService()
	pes.start_listening()