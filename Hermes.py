from User import *
from ClientHandler import *
from Player import *


class Hermes:
    def __init__(self, username):
        self.user = User(username)
        self.client = ClientHandler(self.user)
        self.player = Player()

    def intersect(self, res, inp):
        if len(res) == 0:
            for row in inp:
                res.add(row)
        else:
            temp = set()
            for row in inp:
                temp.add(row)
            res = res.intersection(temp)
        return res

    def search(self, tail):
        Art_res = set()
        Alb_res = set()
        Tra_res = set()
        tail = str(tail)
        for word in tail.split():
            all_rows = self.user.library_get('artist', [], 'artist', ['artist'], word)
            Art_res = self.intersect(Art_res, all_rows)

            all_rows = self.user.library_get('album', ['artist'], 'album', ['album'], word)
            Alb_res = self.intersect(Alb_res, all_rows)

            all_rows = self.user.library_get('streamid', ['artist', 'album', 'title', 'tracknum', 'art', 'location'],
                                             'title',
                                             ['artist', 'album', 'tracknum'], word)
            Tra_res = self.intersect(Tra_res, all_rows)

        # recent_Art, recent_Alb, recent_Tra = Print_Results(Art_res, Alb_res, Tra_res)

        Alb_res2 = set()

        for album in Alb_res:
            albuma = self.user.library_get('album', ['artist', 'art'], 'album', [], album[0], True)
            Alb_res2.add(albuma)

        return [Art_res, Alb_res2, Tra_res]

    def search_album(self, album):
        Art_res = set()
        Alb_res = set()
        Tra_res = set()
        tail = str(album)
        for word in tail.split():
            all_rows = self.user.library_get('artist', [], 'album', ['artist'], word)
            Art_res = self.intersect(Art_res, all_rows)

            all_rows = self.user.library_get('album', ['artist'], 'album', ['album'], word)
            Alb_res = self.intersect(Alb_res, all_rows)

            all_rows = self.user.library_get('streamid', ['artist', 'album', 'title', 'tracknum', 'art', 'location'],
                                             'album',
                                             ['artist', 'album', 'tracknum'], word)
            Tra_res = self.intersect(Tra_res, all_rows)

        # recent_Art, recent_Alb, recent_Tra = Print_Results(Art_res, Alb_res, Tra_res)

        Alb_res2 = set()

        for album in Alb_res:
            albuma = self.user.library_get('album', ['artist', 'art'], 'album', [], album[0], True)
            Alb_res2.add(albuma)

        return [Art_res, Alb_res2, Tra_res]

    def search_artist(self, album):
        Art_res = set()
        Alb_res = set()
        Tra_res = set()
        tail = str(album)
        for word in tail.split():
            all_rows = self.user.library_get('artist', [], 'artist', ['artist'], word)
            Art_res = self.intersect(Art_res, all_rows)

            all_rows = self.user.library_get('album', ['artist'], 'artist', ['album'], word)
            Alb_res = self.intersect(Alb_res, all_rows)

            all_rows = self.user.library_get('streamid', ['artist', 'album', 'title', 'tracknum', 'art', 'location'],
                                             'artist',
                                             ['artist', 'album', 'tracknum'], word)
            Tra_res = self.intersect(Tra_res, all_rows)

        Alb_res2 = set()

        for album in Alb_res:
            albuma = self.user.library_get('album', ['artist', 'art'], 'album', [], album[0], True)
            Alb_res2.add(albuma)

        # recent_Art, recent_Alb, recent_Tra = Print_Results(Art_res, Alb_res, Tra_res)

        return [Art_res, Alb_res2, Tra_res]

    def sync(self):
        print "Syncing"
        self.user.sync(self.client)
        print "Done"

    def syncStream(self):
        self.user.sync_stream(self.client)
        all_rows = self.user.library_get('streamid', ['artist', 'album', 'title', 'tracknum', 'art', 'location'], 'location', ['artist', 'album', 'tracknum'], 'S', False, 'stream')
        return all_rows

    def quit(self):
        self.user.cursor.execute('''DROP TABLE IF EXISTS stream''')
        self.user.db.close()
        # if self.player.Queue != 'stream':
        #     self.player.Queue.save()
