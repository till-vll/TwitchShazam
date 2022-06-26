from keys import tw_client_id,tw_client_secret
import requests

class Twitch_Api: #https://dev.twitch.tv/docs/api/reference#get-streams
    
    def __init__(self, channel_name:str) -> None:
        '''Setup twitch API headers and channel name & ID'''
        self.authentication_paramameters = {"client_id": tw_client_id,
                    "client_secret": tw_client_secret,
                    "grant_type": "client_credentials"
                    }
        self.channel_name = channel_name
        self.channel_id = self.get_channel_id()

    def make_api_request(self, url): #https://stackoverflow.com/a/65117673
        '''Makes a API request to twitch and returns the .json data'''
        authentication_URL = "https://id.twitch.tv/oauth2/token"
        authentication_call = requests.post(url=authentication_URL, params=self.authentication_paramameters) 
        access_token = authentication_call.json()["access_token"]
        head = {
            'Client-ID' : tw_client_id,
            'Authorization' :  "Bearer " + access_token
            }
        request = requests.get(url, headers = head).json()["data"]

        return request
    
    def get_channel_id(self):
        '''Gets the channel ID from the twitch username'''
        request = self.make_api_request( f"https://api.twitch.tv/helix/users?login={self.channel_name}" )
        try: 
            request = request[0]
            channel_id = request["id"]
            return channel_id
        except IndexError:
            print("User not found")   
            return None

    def get_song(self): #Work in progress
        '''Returns the current track using twitch API (BETA)'''
        if self.channel_id == None:
            return None
        song = self.make_api_request(f"https://api.twitch.tv/helix/soundtrack/current_track?broadcaster_id={self.channel_id}")
        return song

    
    def check_mature(self):
        '''Checks if a stream is 18+'''
        if self.channel_id == None:
            return None
        
        request = self.make_api_request(f"https://api.twitch.tv/helix/streams?user_login={self.channel_name}")
        request = request[0]
        if request["is_mature"] == True:
            return True
        else:
            return False

    def check_live(self):
        '''Checks if the streamer is currently live'''
        if self.channel_id == None:
            return None
        
        request = self.make_api_request(f"https://api.twitch.tv/helix/streams?user_login={self.channel_name}")
        try:
            request = request[0]
        except IndexError:
            return False
        if request["type"] == "live":
            return True
        else:
            return False
    

#test = Twitch_Api("noway4u_sir")
#print(test.check_live())
