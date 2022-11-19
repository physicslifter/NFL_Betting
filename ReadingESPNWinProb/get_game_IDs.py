
from selenium import webdriver
from selenium.webdriver.common import keys, by
Keys,  By = keys.Keys(), by.By()
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

week = str(input('What week do you want to look for?'))
year = str(input("What year do you want to look to for?"))

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
url = f"https://www.espn.com/nfl/scoreboard/_/week/{week}/year/{year}/seasontype/2"
d.get_http(url)
game_elements = d.driver.find_elements(By.CLASS_NAME, "Scoreboard")
print('=============================')
print(type(game_elements))
import pdb
pdb.set_trace()
print('=============================')
for element in game_elements:
    print('--')
    print(element.get_attribute("id"))