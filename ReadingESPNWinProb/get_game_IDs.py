from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import numpy as np

year = 2022
week = input("What week do you want to look for?")

url = f"https://www.espn.com/nfl/scoreboard/_/week/{week}/year/{year}/seasontype/2"
options = webdriver.ChromeOptions()
options.add_experimental_option(
    'excludeSwitches', 
    ['enable-logging'])
driver = webdriver.Chrome(
    executable_path='../chromedriver_win32/chromedriver', 
    options = options)
desired_http = 'https://www.espn.com/nfl/game/_/gameId/' + gameID
driver.get(desired_http)
    