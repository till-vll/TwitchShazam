import string
import requests
from keys import youtube_key
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
#https://developers.google.com/youtube/v3/docs

class Youtube_Playlist():
    def __init__(self, streamer_name) -> None:
        self.streamer_name = streamer_name
        self.youtube = self.get_credentials()
    
    def get_video_ID(self, song:dict):
        '''Returns the most relevant Youtube VideoID of a music video'''
        request = self.youtube.search().list(
        part="snippet",
        maxResults=1,
        q= f'{song["title"]} by {song["artist"]}',
        safeSearch="none",
        type="video",
        )
        response = request.execute()
        try:
            video_ID = response["items"][0]["id"]["videoId"]
            return video_ID
        except IndexError:
            print("Song not found")
            return None
    
    def check_playlist(self):
        '''Checks if there is already a playlist created. Returns true if it exsists'''

        request = self.youtube.playlists().list(
            part="snippet",
            mine=True
        )
        response = request.execute()
        playlists = response["items"]
        for playlist in playlists:
            playlist_name = playlist["snippet"]["title"]
            if playlist_name == f"{self.streamer_name.capitalize()} Playlist":
                return playlist["id"]
        return False

    def get_credentials(self):
        '''Get credentials to gain access to google account'''
        scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "twitch_shazam/client_secret_file.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        return youtube
    
    def creat_playlist(self):
        '''Creates a new Playlist for the streamer'''
        request = self.youtube.playlists().insert(
            part="snippet",
            body={
            "snippet": {
                "title": f"{self.streamer_name.capitalize()} Playlist",
                "description": f"Songs from the Twitch channel {self.streamer_name}"
            }
            }
        )
        response = request.execute()
        return response["id"]
    
    def get_songs_in_playlist(self, id):
        '''returns the ids of songs in a playlist'''
        
        song_ids_in_playlist = []
        request = self.youtube.playlistItems().list(
        part="snippet",
        playlistId=id
        )
        response = request.execute()
        items = response["items"]
        
        for item in items:
            song_id = item["snippet"]["resourceId"]["videoId"]
            song_ids_in_playlist.append(song_id)
        
        return song_ids_in_playlist
    
    def add_songs(self, songs):
        '''creates a playlist if necessary and then adds the songs not yet present in the playlist'''
        
        song_ids = []
        if self.check_playlist() == False: #looks for a playlist attributed to the streamer and creates a new if necessary
            playlist_id = self.creat_playlist()
            print("Playlist created")
        else:
            playlist_id = self.check_playlist()

        for song in songs: #create list with song ids from song dict list
            song_id = self.get_video_ID(song)
            song_ids.append(song_id)
        
        song_ids_in_playlist = self.get_songs_in_playlist(playlist_id) #creates a list of song ids already in playlist
        
        for song_id in song_ids: #removes unecessary songs
            if song_id in song_ids_in_playlist:
                song_ids.remove(song_id)
        
        for song_id in song_ids: #adds each song to the playlist
            request = self.youtube.playlistItems().insert(
                part="snippet",
                body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                    "kind": "youtube#video",
                    "videoId": song_id,
                    }
                }
                }
            )
            response = request.execute()
        

# songs = [
#     {'title': 'Maiden Voyage (Future Horizons 340)', 'artist': 'New World, Nirav Sheth & NlightN'},
#     {'title': 'Love Rework', 'artist': 'Chill Children & jhfly'}, 
#     {'title': 'Samba To Massage Your Mate By', 'artist': 'Wun Two'}, 
#     {'title': 'Rain & Flowers', 'artist': 'Tomppabeats'}, 
#     {'title': 'Stars', 'artist': 'Bahwee'}, 
#     {'title': 'Latenightwalking', 'artist': 'Melodiesinfonie'}, 
#     {'title': 'Fly Away', 'artist': 'GlobulDub'}, 
#     {'title': 'Departure', 'artist': 'Chinsaku'}, 
#     {'title': '2 A.m.', 'artist': 'weirdjack'}, 
#     {'title': 'Confidence', 'artist': 'Kuranes'}, 
#     {'title': 'Idkanymore', 'artist': 'Knowmadic'}, 
#     {'title': 'El Vuelo', 'artist': 'IAmNotARobot'}, 
#     {'title': 'Embryo (Subp Yao Remix)', 'artist': 'The Science & Subp Yao'}, 
#     {'title': "Let's Survive", 'artist': 'Sweeps'}, 
#     {'title': 'Woah', 'artist': 'Engelwood & Jeff Kaale'}, 
#     {'title': 'Purificando Aura Con Piano', 'artist': 'PURIFICAR EL AURA'}, 
#     {'title': 'Animo Y Emoción', 'artist': 'Levantando tu animo'}, 
#     {'title': 'Stars', 'artist': 'Maxwell Young'}, 
#     {'title': "You'll Be Fine", 'artist': 'daz.chill'}, 
#     {'title': 'Living Life', 'artist': 'K.wood Feat. Josh Anthony & Suave'}
# ]

# test = Youtube_Playlist(songs,"test10")

# test.add_songs()
