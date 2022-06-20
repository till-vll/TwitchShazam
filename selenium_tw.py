from keys import chrome_driver_path
from pyparsing import Opt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pyshadow.main import Shadow
from time import sleep
from twitch_api import Twitch_Api

class Selenium_tw(Twitch_Api):
    def __init__(self, channel_name:str) -> None:
        '''Setup selenium browser. Requires streamer to listen to and if that streamer has a +18 banner. Opens witch, acccepts cookies and extension sets shortcut'''
        Twitch_Api.__init__(self, channel_name)
        
        #if the username cannot be found -> id == None, so Selenium won't init
        if self.check_live(): 
            
            #setup selenium https://stackoverflow.com/a/44363549
            options = Options()
            options.add_extension("Shazam.crx")
            options.add_extension("Twitch-Adblock.crx")
            self.driver = webdriver.Chrome(chrome_driver_path,options=options)
            self.driver.implicitly_wait(10)
            self.wait = WebDriverWait(self.driver, 10)
            
            #setup twitch 
            self.driver.get(f"https://twitch.com/{self.channel_name}")
            self.accept_cookies()
            if self.check_mature():
                self.accept_age()
            
            if "twitch.tv" in self.driver.current_url:
                self.main_window = self.driver.window_handles[0]
                self.extension = self.driver.window_handles[1]
            else:
                self.main_window = self.driver.window_handles[1]
                self.extension = self.driver.window_handles[0]
            self.set_shortcut()
       
    def accept_cookies(self):
        '''Accepts Cookies'''
        cookie_butt = self.wait.until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[1]/div/div/div/div[3]/button')))
        cookie_butt.click()

    def accept_age(self):
        '''Accepts 18+ if necessary'''
        age_butt = self.wait.until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div[1]/main/div[2]/div[3]/div/div/div[2]/div/div[2]/div/div[2]/div/div/div[5]/div/div[3]/button')))
        age_butt.click()
    
    def set_low_settings(self): #TODO set low settings
        '''Sets stream video settings to minimum'''
        pass
    
    def perform_shortcut(self):
        '''Performs the shortcut alt + k'''
        actions = ActionChains(self.driver)
        actions.key_down(Keys.ALT).perform()
        sleep(0.5)
        actions.key_down("k").perform()
        sleep(0.5)
        actions.key_up(Keys.ALT).perform()
        sleep(0.5)
        actions.key_up('k').perform()
    
    def try_shazam(self):
        '''Calls the Shazam extension with the shortcut that has been set and waits 15 seconds.'''
        actions = ActionChains(self.driver)
        #actions.click().perform()
        self.perform_shortcut()
        sleep(15)
        self.perform_shortcut()

    def set_shortcut(self):
        '''Sets the shortcut of the extension so you can access it later'''
        url = "chrome://extensions/shortcuts"
        sleep(0.5)
        self.driver.switch_to.window(self.extension) #switches to the window of the twitch adblock extension
        sleep(0.5)
        #opens chrome shortcut page
        self.driver.get(url)
        self.driver.maximize_window()
        shadown = Shadow(self.driver) #https://pypi.org/project/pyshadow/
        
        #sets the shortcut
        edit_butt = self.wait.until(EC.element_to_be_clickable(shadown.find_element('#edit')))
        edit_butt.click()
        self.perform_shortcut()
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
for i in range(3):
    test.try_shazam()
    sleep(15)

# print(songs)
# sleep(1000)