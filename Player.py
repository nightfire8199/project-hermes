# from Library import *

import vlc


class Player:
    def __init__(self):
        self.vlc = vlc.MediaPlayer()
        self.events = self.vlc.event_manager()

    def play_track(self, url):
        self.vlc.set_mrl(url)
        self.play()

    def play(self):
        self.vlc.play()

    def pause(self):
        self.vlc.pause()

    def stop(self):
        self.vlc.stop()