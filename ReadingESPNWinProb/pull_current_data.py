from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option(
    'excludeSwitches', 
    ['enable-logging'])
driver = webdriver.Chrome(
    executable_path='../chromedriver_win32/chromedriver', 
    options = options)
driver.get('https://www.espn.com/nfl/game/_/gameId/401437752')


current_play_text = driver.find_element(By.XPATH, "//*[@id='gameFlowPopup-185']/div[3]/p[2]")
status_text = driver.find_element(By.XPATH, "//*[@id='gameFlowPopup-185']/div[1]/h5")

print(f'current play: {current_play_text.text}')
print(f'status: {status_text.text}')
