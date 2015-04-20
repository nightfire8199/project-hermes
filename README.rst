project-hermes
==============

A multi-sourced music management system written in python

Installation Instructions
-------------------------

Install Dependencies::

	$ pip install soundcloud
	$ pip install gmusicapi
	$ pip install pyopenssl ndg-httpsclient pyasn1


Get a Soundcloud Client ID:

Go to http://soundcloud.com/you/apps and register a new app to get a client ID

To run the program the first time::

	$ python Hermes.py


The program will ask you to build a User Profile upon first run. 

WARNING: USER PROFILES ARE STORED IN PLAIN TEXT

To run the program after a User Profile exists to auto-login::

	$ python Hermes.py [user-profile-name]

Eventually you will be greeted with a command prompt. 

On first run of Hermes, you must build your library. To do so type::

	$> sync


Type non-command strings to search your library...

Type::

	$> play [song-id]

To play a song

Type::

	$> pause
	$> stop
	$> play 

To control the current track


Type::
	
	$> add [song-id]
	$> start
	$> print


To control the queue

Type::

	$> quit

To exit
