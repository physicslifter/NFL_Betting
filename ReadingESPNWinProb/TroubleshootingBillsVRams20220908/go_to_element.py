from selenium import webdriver
from selenium.webdriver.common import keys, by
Keys,  By = keys.Keys(), by.By()
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service

url = "://www.espn.com/nfl/game/_/gameId/401437654"


class DriverHandler:
    '''
    For handling driver setup & changing
    '''
    def __init__(self):
        self.s = Service('../chromedriver_win32_107/chromedriver.exe')

    def get_http(self, http_address):
        self.driver = webdriver.Chrome(service=self.s)
        self.driver.get(http_address)

d = DriverHandler()
d.get_http(url)
