from keys import chrome_driver_path
from pyparsing import Opt
from keys import chrome_driver_path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pyshadow.main import Shadow
from pykeyboard import PyKeyboard #https://pypi.org/project/PyUserInput/
from time import sleep
from twitch_api import Twitch_Api

class Selenium_tw(Twitch_Api):
    def __init__(self, channel_name:str) -> None:
        '''Setup selenium browser. Requires streamer to listen to and if that streamer has a +18 banner. Opens witch, acccepts cookies and extension sets shortcut'''
        Twitch_Api.__init__(self, channel_name)
        #setup selenium https://stackoverflow.com/a/44363549
        options = Options()
        options.add_extension("Shazam.crx")
        options.add_extension("Twitch-Adblock.crx")
        self.driver = webdriver.Chrome(chrome_driver_path,options=options)
        self.wait = WebDriverWait(self.driver, 10)
        
        #if the username cannot be found -> id == None, so Selenium won't init
        if self.check_live(): 
            
            
            #setup twitch 
            self.driver.get(f"https://twitch.com/{self.channel_name}")
            self.main_window = self.driver.window_handles[0]
            self.extension = self.driver.window_handles[1]
            self.accept_cookies()
            if self.check_mature():
                self.accept_age()
            self.set_shortcut()
       
    def accept_cookies(self):
        '''Accepts Cookies'''
        cookie_butt = self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[1]/div/div/div/div[3]/button')
        self.wait.until(EC.element_to_be_clickable(cookie_butt))
        cookie_butt.click()
    
    def accept_age(self):
        '''Accepts 18+ if necessary'''
        sleep(5)
        age_butt = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[1]/main/div[2]/div[3]/div/div/div[2]/div/div[2]/div/div[2]/div/div/div[5]/div/div[3]/button')
        self.wait.until(EC.element_to_be_clickable(age_butt))
        age_butt.click()
    
    def set_low_settings(self): #TODO set low settings
        '''Sets stream video settings to minimum'''
        pass
    
    def try_shazam(self):
        '''Calls the Shazam extension with the shortcut that has been set and waits 15 seconds.'''
        k = PyKeyboard()
        #Open extension
        k.press_key(k.alt_key)
        k.press_key("K")
        sleep(1)
        k.release_key(k.alt_key)
        k.release_key("K")
        
        #wait 15 seconds to find song
        sleep(15)
        
        #closes the extension
        k.press_key(k.alt_key)
        k.press_key("K")
        sleep(1)
        k.release_key(k.alt_key)
        k.release_key("K")

    
    def set_shortcut(self):
        '''Sets the shortcut of the extension so you can access it later'''
        url = "chrome://extensions/shortcuts"
        self.driver.switch_to.window(self.extension) #switches to the window of the twitch adblock extension
        sleep(3)
        
        #opens chrome shortcut page
        self.driver.get(url)
        self.driver.maximize_window()
        shadown = Shadow(self.driver) #https://pypi.org/project/pyshadow/
        
        #sets the shortcut 
        edit_butt = shadown.find_element('#edit')
        sleep(1)
        edit_butt.click()
        sleep(1)
        k = PyKeyboard()
        k.press_key(k.alt_key)
        k.press_key("K")
        sleep(1)
        k.release_key(k.alt_key)
        k.release_key("K")
        sleep(1)
        
        #closes the window and switches back to twitch
        self.driver.close()
        self.driver.switch_to.window(self.main_window)
    
    def close_all(self):
        '''Closes all Selenium windows'''
        self.driver.quit()
    
    def get_songs(self):
        '''Returns the Songs in a list as a dict with Song title and artist'''
        songs = []
        #open the extension popup as a window
        self.driver.get("chrome-extension://mmioliijnhnoblpgimnlajmefafdfilb/popup.html")
        sleep(1)
        #open container
        container_butt = self.driver.find_element(By.XPATH,'/html/body/div/div[2]/div[1]/div[1]')
        container_butt.click()
        #look for all song containers
        items = self.driver.find_elements(By.CLASS_NAME,"text-content")
        sleep(1)
        #go through all containers and add the song dict to the list
        for item in items:
            title = item.find_element(By.CSS_SELECTOR,"#title").text
            artist = item.find_element(By.CSS_SELECTOR,"#artist").text
            song = {
                "title": title,
                "artist": artist
            }
            songs.append(song)
        
        return songs




test = Selenium_tw("noway4u_sir")
if test.check_live():
    for i in range(3):
        test.try_shazam()
        sleep(15)
else:
    test.close_all()

# songs = test.get_songs()
# print(songs)
# sleep(1000)