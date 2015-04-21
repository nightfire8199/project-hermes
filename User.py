from gmusicapi import Webclient
import vlc
import sys
import os
from os import path
import getpass

class User:
	
	def __init__(self):
		self.library = []
		self.G_username = ""
		self.G_password = ""
		self.S_username = ""
		self.S_password = ""
		self.GOOGLE_DEVICE_ID = ""
		self.SOUNDCLOUD_CLIENT_ID = ""
		self.SOUNDCLOUD_CLIENT_SECRET_ID = ""
		self.userdata_path = path.join('..', 'hermes-userdata')
		if(len(sys.argv) >= 2):
			try:
				File = open(self.get_filename(str(sys.argv[1])))
			except IOError:
				print 'Cannot find user: ' + str(sys.argv[1])
				print 'Creating new user...'
				# filename = raw_input('Choose a user profile filename: ')
				self.authenticate(self.get_filename())
			else:
				self.login(self.get_filename(str(sys.argv[1])))

		else:
			# filename = path.join('../', raw_input('Choose a user profile filename: '))
			self.authenticate(self.get_filename())

	def get_filename(self, arg=None):
		if arg is None:
			arg = raw_input('Choose a user profile filename: ')
		self.profile_name = arg
		if not path.exists(self.userdata_path):
			os.mkdir(self.userdata_path)

		return path.join(self.userdata_path, arg)

	def login(self,USER_DATA_FILENAME):
		File = open(USER_DATA_FILENAME,'r')
		self.G_username = File.readline().rstrip('\n')
		self.G_password = File.readline().rstrip('\n')
		self.S_username = File.readline().rstrip('\n')
		self.S_password = File.readline().rstrip('\n')
		self.GOOGLE_DEVICE_ID = File.readline().rstrip('\n')
		self.SOUNDCLOUD_CLIENT_ID = File.readline().rstrip('\n')
		self.SOUNDCLOUD_CLIENT_SECRET_ID = File.readline().rstrip('\n')
		File.close()
		

	def authenticate(self,USER_DATA_FILENAME):
		self.G_username = raw_input("Google Play Account Email: ")
		self.G_password = getpass.getpass("Google Play Account Pass: ")

		Deviceclient = Webclient()
		Deviceclient.login(self.G_username,self.G_password)

		DList = Deviceclient.get_registered_devices()	

		for device in DList:	
			if device['type'] == "PHONE":
				self.GOOGLE_DEVICE_ID = device["id"]
				if self.GOOGLE_DEVICE_ID[:2] == '0x':
					self.GOOGLE_DEVICE_ID = self.GOOGLE_DEVICE_ID[2:]
				break

		self.S_username = raw_input("Soundcloud Account Username: ")
		self.S_password = getpass.getpass("Soundcloud Account Password: ")
		self.SOUNDCLOUD_CLIENT_ID = raw_input("Soundcloud Client ID: ")
		self.SOUNDCLOUD_CLIENT_SECRET_ID = raw_input("Soundcloud Secret Client ID: ")

		File = open(USER_DATA_FILENAME,'w+')
		File.write(self.G_username + '\n')
		File.write(self.G_password + '\n')
		File.write(self.S_username + '\n')
		File.write(self.S_password + '\n')
		File.write(self.GOOGLE_DEVICE_ID + '\n')
		File.write(self.SOUNDCLOUD_CLIENT_ID + '\n')
		File.write(self.SOUNDCLOUD_CLIENT_SECRET_ID + '\n')
		File.close()

	def get_command(self,_command):
		pass
