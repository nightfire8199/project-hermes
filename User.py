from gmusicapi import Webclient
from Playlist import *
import soundcloud

import eyeD3

import sys
import os
import sqlite3
from os import path
import getpass
import base64
import pickle


class User:
    def __init__(self, username):
        self.profile_name = username
        self.G_username = ""
        self.G_password = ""
        self.S_username = ""
        self.S_password = ""
        self.GOOGLE_DEVICE_ID = ""
        self.SOUNDCLOUD_CLIENT_ID = ""
        self.SOUNDCLOUD_CLIENT_SECRET_ID = ""
        self.enc_key = "private_key"

        self.playlists = []
        self.watched = []

        # if len(sys.argv) >= 2:
        #     try:
        #         File = open(self.get_filename(str(sys.argv[1])))
        #     except IOError:
        #         print 'Cannot find user: ' + str(sys.argv[1])
        #         print 'Creating new user...'
        #         self.authenticate(self.get_filename())
        #     else:
        #         self.login(self.get_filename(str(sys.argv[1])))
        # else:
        #     self.authenticate(self.get_filename())

        self.userdata_path = path.join('..', 'hermes-userdata', username)
        print self.userdata_path
        if not path.exists(self.userdata_path):
            os.mkdir(self.userdata_path)

        profilePath = path.join(self.userdata_path, self.profile_name)
        self.login(profilePath)

        self.db_path = path.join(self.userdata_path, self.profile_name + '_db')
        self.db = sqlite3.connect(self.db_path)
        self.cursor = self.db.cursor()

        self.watched_file = path.join(self.userdata_path, self.profile_name + "_watched")

        if not path.exists(self.watched_file):
            open(self.watched_file, 'w').close()

        if os.stat(self.watched_file).st_size > 0:
            filer = open(self.watched_file, 'r')
            self.watched = pickle.load(filer)
            filer.close()

        for filer in os.listdir(self.userdata_path):
            if filer.startswith("playlist_"):
                #print "Adding playlist " , file
                playlist = Playlist(filer, self)
                self.playlists.append(playlist)

    def get_filename(username):
        return path.join('..', 'hermes-userdata', username)
    get_filename = staticmethod(get_filename)

    def encode(key, clear):
        enc = []
        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc))

    encode = staticmethod(encode)

    def decode(self, key, enc):
        dec = []
        enc = base64.urlsafe_b64decode(enc)
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)

    def authenticate(self, USER_DATA_FILENAME):
        self.G_username = raw_input("Google Play Account Email: ")
        self.G_password = getpass.getpass("Google Play Account Pass: ")

        Deviceclient = Webclient()
        Deviceclient.login(self.G_username, self.G_password)

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

        File = open(USER_DATA_FILENAME, 'w+')
        File.write(self.encode(self.enc_key, self.G_username) + '\n')
        File.write(self.encode(self.enc_key, self.G_password) + '\n')
        File.write(self.encode(self.enc_key, self.S_username) + '\n')
        File.write(self.encode(self.enc_key, self.S_password) + '\n')
        File.write(self.GOOGLE_DEVICE_ID + '\n')
        File.write(self.SOUNDCLOUD_CLIENT_ID + '\n')
        File.write(self.SOUNDCLOUD_CLIENT_SECRET_ID + '\n')
        File.close()

    def login(self, USER_DATA_FILENAME):
        File = open(USER_DATA_FILENAME, 'r')
        self.G_username = self.decode(self.enc_key, File.readline().rstrip('\n'))
        self.G_password = self.decode(self.enc_key, File.readline().rstrip('\n'))
        self.S_username = self.decode(self.enc_key, File.readline().rstrip('\n'))
        self.S_password = self.decode(self.enc_key, File.readline().rstrip('\n'))
        self.GOOGLE_DEVICE_ID = File.readline().rstrip('\n')
        self.SOUNDCLOUD_CLIENT_ID = File.readline().rstrip('\n')
        self.SOUNDCLOUD_CLIENT_SECRET_ID = File.readline().rstrip('\n')
        File.close()

    def library_get(self, distinct, get_others, where_like, ordered_return, USI, single=False, db='tracks'):
        query = 'SELECT DISTINCT(' + distinct + ')'
        for item in get_others:
            query += ', ' + item
        query += ' FROM ' + db + ' WHERE ' + where_like + ' LIKE ? OR ' + where_like + ' LIKE ?'
        if len(ordered_return) > 0:
            query += ' ORDER BY '
            for item in ordered_return:
                query += item + ', '
            query = query[:len(query) - 2]
        self.cursor.execute(query, (USI + '%', '% ' + USI + '%',))
        if single is False:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def sync(self, client):
        L_list = []
        for path in self.watched:
            filelist = []
            for (dirpath, dirnames, filenames) in os.walk(path):
                filelist.extend(dirpath + '/' + filename for filename in filenames)
            L_list += filelist

        for File in L_list:
            if not (File.endswith('mp3') or File.endswith('wav')):
                L_list.remove(File)

        G_list = client.G_client.get_all_songs()

        Fav_Size = 0
        S_list = client.S_client.get('/me/favorites', limit=300)
        while Fav_Size != len(S_list):
            Fav_Size = len(S_list)
            S_list += client.S_client.get('/me/favorites', limit=300, offset=len(S_list))

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tracks(id INTEGER PRIMARY KEY, title TEXT, album TEXT, artist TEXT, location TEXT, streamid TEXT UNIQUE, tracknum INTEGER, art TExT)''')
        self.cursor.execute('''SELECT count(*) FROM tracks''')
        iden = self.cursor.fetchone()[0]
        for track in G_list:
            art = ''
            try:
                art = track['albumArtRef'][0]['url']
            except KeyError:
                art = ''
            self.cursor.execute('''INSERT OR IGNORE INTO tracks VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
                                (iden, track['title'], track['album'], track['artist'], 'G', 'G_' + str(track['id']), track['trackNumber'], art))
            iden += 1

        for track in S_list:
            self.cursor.execute('''INSERT OR IGNORE INTO tracks VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
                                (iden, track.title, "Unknown Album", track.user['username'], 'S', 'S_' + str(track.id), 0, track.artwork_url))
            iden += 1

        for track in L_list:
            tag = eyeD3.Tag()
            tag.link(track)
            if len(tag.getArtist()) and len(tag.getAlbum()) and len(tag.getTitle()) > 0:
                self.cursor.execute('''INSERT OR IGNORE INTO tracks VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
                                    (iden, tag.getTitle(), tag.getAlbum(), tag.getArtist(), 'L', 'L_' + str(track), tag.track_num[0], ''))
                iden += 1
            else:
                print "Could not resolve track metadata for: " + track

        self.db.commit()

    def sync_stream(self, client):
        self.cursor.execute('''DROP TABLE IF EXISTS stream''')
        self.db.commit()

        tracks = client.S_client.get('/me/activities/tracks/affiliated', limit=200)

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stream(id INTEGER PRIMARY KEY, title TEXT, album TEXT,artist TEXT, location TEXT, streamid TEXT, tracknum INTEGER, art TEXT)''')

        iden = 0
        duplifier = []
        for track in tracks.obj['collection']:
            if track['origin']['id'] in duplifier:
                continue
            if track['origin']['kind'] == 'playlist':

                Playtracks = client.S_client.get('/playlists/99297471/tracks')
                for play in Playtracks:
                    if play.id in duplifier:
                        continue
                    self.cursor.execute('''INSERT OR IGNORE INTO stream VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
                                        (iden, play.title, "Unknown Album", play.user['username'], 'S', 'S_' + str(play.id), 0, play.artwork_url))
                    self.db.commit()

                    duplifier.append(play.id)
                    duplifier.append(track['origin']['id'])
                    iden += 1
            else:
                self.cursor.execute('''INSERT OR IGNORE INTO stream VALUES(?, ?, ?, ?, ?, ?, ?, ?)''',
                                    (iden, track['origin']['title'], "Unknown Album", track['origin']['user']['username'], 's', 's_' + str(track['origin']['id']), 0, track['origin']['artwork_url']))
                self.db.commit()

                duplifier.append(track['origin']['id'])
                iden += 1
            if iden == 50:
                break

        self.db.commit()

    def add_watched(self, directory):
        # already there
        if directory in self.watched:
            return False

        self.watched.append(directory)
        self.save_watched()
        return True

    def remove_watched(self, directory):
        self.watched.remove(directory)
        self.save_watched()

    def save_watched(self):
        filer = open(self.watched_file, 'w')
        pickle.dump(self.watched, filer)
        filer.close()
