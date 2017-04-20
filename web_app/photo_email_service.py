from extensions import connect_to_database
from email.mime.text import MIMEText
from api.model import uploads3
from os.path import basename
import threading
import smtplib
import zipfile
import poplib
import boto3
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

Please note that you may only upload one set of photos at a time. If you upload another set, the photos you just uploaded will be overwritten.

In other words, please make sure to convert the set of 2D photos you just uploaded to a 3D model before uploading another set of photos.

Happy modeling!
'''

EMAIL_SUBJECT_SUCCESS = 'Photos successfully uploaded to website!'
EMAIL_BODY_SUCCESS = '''
Thank your for submitting your photos.

You can access them on our website.

Happy modeling!
'''

# Use ./photos when testing locally 
# (note the '.'; this prevents a permission issue from being raised on local machines)
IMAGE_PATH = './home/ubuntu/photos/'

class PhotoEmailService:
	def __init__(self):
		self.db = connect_to_database()
		if not os.path.exists(IMAGE_PATH):
			os.makedirs(IMAGE_PATH)

	# Adds photos in local storage to a zipfile, uploads that zipfile to S3,
	# puts that zipfiles data into PhotoZip table, and then deletes the 
	# zipfile and photos from temporary local storage
	def add_to_s3_and_database(self, username, photo_number):
		# Create new zipfile
		zipfile_name = 'photos_{0}.zip'.format(username)
		zipfile_path_and_name = os.path.join(IMAGE_PATH, zipfile_name)
		zf = zipfile.ZipFile(zipfile_path_and_name, mode='w')

		# Add photos to zipfile, deleting them from temporary local storage as we go
		for pn in range(0, photo_number):
			filename = 'photo_{0}.jpg'.format(pn)
			photo_path_and_name = os.path.join(IMAGE_PATH, filename)
			zf.write(photo_path_and_name, basename(photo_path_and_name))
			os.remove(photo_path_and_name)
		zf.close()

		# Upload user's photos zipfile to user's S3 photo bucket and construct its S3 URL
		s3_client = boto3.client('s3')
		s3_client.upload_file(zipfile_path_and_name, 'babyhead', zipfile_name)
		url = 'https://s3.amazonaws.com/babyhead/{0}'.format(zipfile_name)
		print('\nUploaded zipfile to:\n{0}\n'.format(url))

		# Insert this zipfile's data into the database (clean database beforehand)
		cur = self.db.cursor()
		cur.execute('DELETE FROM PhotoZip WHERE username=\'{}\''.format(username))
		cur = self.db.cursor()
		cur.execute('INSERT INTO PhotoZip (username, url) VALUES ' + 
					'(\'{0}\', \'{1}\')'.format(username, url))

		# Delete zipfile from temporary local storage
		os.remove(zipfile_path_and_name)

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
		if emails > 0:
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

			# Skip this email and process next email if we can't find a user with 
			# the same email address as the sender
			results = cur.fetchall()
			if len(results) == 0:
				print(	'Sending \"Failed upload\" email. Reason: no user found with this email address\n' + 
						'sender address was: {0}'.format(sender_address))
				self.send_email(sender_address,
								EMAIL_SUBJECT_INVALID,
								EMAIL_BODY_INVALID)
				break

			# Otherwise, keep track of the username for the person who sent this email
			username = results[0]['username']

			#------------------------------------#
			# Save attachments if email is valid #
			#------------------------------------#
			email_contains_photos = False
			photo_number = 0
			for part in str_message.walk():
				# Skip parts of email that don't contain file attachments
				if (part.get_content_maintype() == 'multipart'
				or part.get('Content-Disposition') is None):
					continue

				print('Attempting to save the following attachment: {0}'.format(part.get_filename()))

				email_contains_photos = True

				# Save the attached image locally
				filename = 'photo_{0}.jpg'.format(photo_number)
				filename_and_path = os.path.join(IMAGE_PATH, filename)
				fp = open(filename_and_path, 'wb')
				fp.write(part.get_payload(decode=1))
				fp.close()

				photo_number += 1

			# Adds photos in local storage to a zipfile, uploads that zipfile to S3,
			# puts that zipfiles data into PhotoZip table, and then deletes the 
			# zipfile and photos from temporary local storage
			self.add_to_s3_and_database(username, photo_number)

			# Return an error message via email if the email lacked photos
			if not email_contains_photos:
				print('Sending \"Failed upload\" email. Reason: email lacked photos)')
				self.send_email(sender_address, 
								EMAIL_SUBJECT_NO_PHOTOS, 
								EMAIL_BODY_NO_PHOTOS)

			# Let the sender know if their photos were successfully uploaded
			else:
				print('Sending \"Successful upload\" email')
				self.send_email(sender_address,
								EMAIL_SUBJECT_SUCCESS,
								EMAIL_BODY_SUCCESS)

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
