from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option(
    'excludeSwitches', 
    ['enable-logging'])
driver = webdriver.Chrome(
    executable_path='../chromedriver_win32/chromedriver', 
    options = options)
driver.get('https://www.espn.com/nfl/game/_/gameId/401437752')