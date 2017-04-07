from email.mime.text import MIMEText
from extensions import connect_to_database
import smtplib
import poplib
import email
import time
import os

WEB_APP_EMAIL_USERNAME = 'headmodels481@gmail.com'
WEB_APP_EMAIL_PASSWORD = 'eecs481rules!'

EMAIL_SUBJECT_INVALID = 'Photos not uploaded to website'
EMAIL_BODY_INVALID = '''
Thank you for sending us your photos that you'd like to convert to a 3D model.

Unfortunately, it looks like your email address is not associated with a registered account.

If this is the case, please create an account on our website.

If you have an account with us, please try to email your photos from the email address associated with your account.

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
		pass
		#self.db = connect_to_database()

	# Sends an email
	def send_email(self, to_address, subject, body):
		# Create a text/plain message
		msg = MIMEText(body)

		# me == the sender's email address
		# you == the recipient's email address
		msg['Subject'] = subject
		msg['From'] = WEB_APP_EMAIL_USERNAME
		msg['To'] = to_address

		s = smtplib.SMTP('smtp.gmail.com', 587) # Port 587
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login(WEB_APP_EMAIL_USERNAME, WEB_APP_EMAIL_PASSWORD)
		s.send_message(msg)
		s.close()

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
			print('Error connecting to email. Trying again...')
			return
		connection.set_debuglevel(1)
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
			'''
			cur = db.cursor()
			cur.execute('SELECT * FROM User WHERE email=\'{0}\''.format(sender_address))
			if len(cur.fetchall()) == 0:
				# Send invalid email address email
				break
			'''

			#------------------------------------#
			# Save attachments if email is valid #
			#------------------------------------#
			for part in str_message.walk():
				# Skip parts of email that don't contain file attachments
				if (part.get_content_maintype() == 'multipart'
				or part.get('Content-Disposition') is None):
					continue

				filename = part.get_filename()
				'''
				if not filename: 
					filename = "test.txt"
				'''
				print('Attempting to save the following attachment: {0}'.format(filename))

				try:
					self.send_email(sender_address, EMAIL_SUBJECT_SUCCESS, EMAIL_BODY_SUCCESS)
				except:
					print('Error sending email response!')

				savedir="./static/photos/"
				fp = open(os.path.join(savedir, filename), 'wb')
				fp.write(part.get_payload(decode=1))
				fp.close

			# Delete email from consideration for processing.
			# Does not actually delete email from Gmail account.
			connection.dele(i+1)

		# Close the connection. This is required to finalize any email deletions.
		connection.quit()

	# Listens for emails indefinitely and saves photos from new emails
	# to the appropriate locations
	def listen_for_emails(self):
		while True:
			self.save_unread_email_photos()

pes = PhotoEmailService()
pes.listen_for_emails()