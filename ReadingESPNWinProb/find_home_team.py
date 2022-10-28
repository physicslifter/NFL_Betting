#%%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time


default_gameID = '401437752'

def find_home_team(gameID:str):
    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        'excludeSwitches', 
        ['enable-logging'])
    driver = webdriver.Chrome(
        executable_path='../chromedriver_win32/chromedriver', 
        options = options)
    desired_http = 'https://www.espn.com/nfl/game/_/gameId/' + gameID
    driver.get(desired_http)
    away_path = "//*[@id='linescore']/tbody/tr[1]/td[1]"
    home_path = "//*[@id='linescore']/tbody/tr[2]/td[1]"
    home = driver.find_element(By.XPATH, home_path)
    away = driver.find_element(By.XPATH, away_path)
    print(f'home: {home.text} away: {away.text}')
    
    return home.text, away.text
    
find_home_team(default_gameID)
# %%
