from sys import _clear_type_cache
from time import sleep
from selenium_tw import Selenium_tw
from youtube_playlist import Youtube_Playlist

class Twitch_Shazam(Selenium_tw,Youtube_Playlist):
    def __init__(self, channel_name: str) -> None:
        Youtube_Playlist.__init__(self,channel_name)
        Selenium_tw.__init__(self,channel_name)
        self.channel_name = channel_name
        self.songs = []
    
    def shazam_while_live(self):
        while self.check_live():
            self.try_shazam()
            sleep(15)
        self.songs = self.get_songs()
        self.close_all()
    
    def shazam_for_x_times(self,nr_shazams:int):
        for shazam in range(nr_shazams):
            self.try_shazam()
            sleep(15)
        self.songs = self.get_songs()
        self.close_all()

test = Twitch_Shazam("ratirl")

test.shazam_while_live()
print(test.songs)
#test.add_songs(test.songs)
pass