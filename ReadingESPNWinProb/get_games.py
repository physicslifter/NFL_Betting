from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


sample_url = "https://www.espn.com/nfl/scoreboard/_/week/7/year/2022/seasontype/2"
classname = "Scoreboard bg-clr-white flex flex-auto justify-between"
options = webdriver.ChromeOptions()
options.add_experimental_option(
    'excludeSwitches', 
    ['enable-logging'])
s=Service('../chromedriver_win32/chromedriver.exe')
o=webdriver.ChromeOptions()
driver = webdriver.Chrome(service=s, options = o)

'''driver = webdriver.Chrome(
    executable_path='../chromedriver_win32/chromedriver.exe', 
    options = options)'''

url = 'https://www.espn.com/nfl/game/_/gameId/' + id
driver.get(url)

game_elements = driver.find_element(By.CLASSNAME, classname)
for element in game_elements:
    print(element)