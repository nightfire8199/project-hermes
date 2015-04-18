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

To run the program::

	$ python LibraryBuild.py


The program will ask for your various credentials before compiling a library

TODO:

* Build client interface
* Store authentication credentials locally
* Store library track metadata locally 
* Auto-login if credentials stored
* Auto populate if library stored
DONE * Convert master library from a list to a dict
