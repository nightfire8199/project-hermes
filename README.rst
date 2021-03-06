project-hermes
==============

A multi-sourced music management system written in python

Installation Instructions
-------------------------

Install Prerequisites::
	1. vlc media player
	2. PyQt4

Install Dependencies::

	$ pip install soundcloud
	$ pip install gmusicapi
	$ pip install pyopenssl ndg-httpsclient pyasn1
	$ pip install urllib3
	$ pip install eyeD3-pip
	$ pip install pillow
	$ pip install numpy

Note: On Windows it is usually easier to download and install numpy from the installers (.exe) on sourceforge


Get a Soundcloud Client ID:

Go to http://soundcloud.com/you/apps and register a new app to get a client ID

To run the program the first time::

	$ python Hermes.py


The program will ask you to build a User Profile upon first run. 

To run the program after a User Profile exists to auto-login::

	$ python Hermes.py [user-profile-name]

Eventually you will be greeted with a command prompt. 

On first run of Hermes, you must build your library. To do so type::

	$> sync


Type::

	$> search [terms]
	$> view [selection]

To navigate your library

Type::

	$> play [selection]

To play a song

Type::

	$> pause
	$> stop
	$> play 
	$> now

To control the current track


Type::
	
	$> add [selection]
	$> start
	$> clear
	$> print


To control the current playlist

Type::

	$> make [playlist-name]
	$> print playlists
	$> print [playist-name]
	$> add [playlist-name] [selection]

To work with other playlists

Type::

	$> start stream

To start the soundcloud stream

Type::

	$> quit

To exit
