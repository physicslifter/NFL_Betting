from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

'''
This is the first of the scripts and proves that I can
move the cursor
'''

options = webdriver.ChromeOptions()
options.add_experimental_option(
    'excludeSwitches', 
    ['enable-logging'])
driver = webdriver.Chrome(
    executable_path='../chromedriver_win32/chromedriver', 
    options = options)
driver.get('https://www.espn.com/nfl/game/_/gameId/401437752')

print('================================')
print('First showing current play, then scrolling to graph and getting a new play')
print('================================')

current_play_text = driver.find_element(By.XPATH, "//*[@id='gameFlowPopup-185']/div[3]/p[2]")
print(f'current play: {current_play_text.text}')

print('--')

graph_xpath = "//*[@id='gameFlow-graph']/div/div"
plot_element = driver.find_element(By.XPATH, graph_xpath)

actions = ActionChains(driver)
actions.move_to_element(plot_element).perform()

current_play_text = driver.find_element(By.XPATH, "//*[@id='gameFlowPopup-185']/div[3]/p[2]")
print(f'current play: {current_play_text.text}')

print('--')

actions.move_by_offset(-1,0).perform()
current_play_text = driver.find_element(By.XPATH, "//*[@id='gameFlowPopup-185']/div[3]/p[2]")
print(f'current play: {current_play_text.text}')
print('================================')
