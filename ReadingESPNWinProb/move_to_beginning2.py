from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

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

#important/interesting xpaths
most_recent_play_xpath = "//*[@id='gameFlowPopup-185']/div[3]/p[2]" #play data, time, etc
graph_xpath = "//*[@id='gameFlow-graph']/div/div" #The path for the plot play-by-play
percent_xpath = "//*[@id='gameFlowPopup-185']/div[1]/h5"

def print_vals():
    play = driver.find_element(By.XPATH, most_recent_play_xpath)
    percent = driver.find_element(By.XPATH, percent_xpath)
    print('================')
    print(f'Win probability: {percent.text}')
    print(f'Most recent play: {play.text[0:12]}')
    
def get_vals():
    play = driver.find_element(By.XPATH, most_recent_play_xpath)
    percent = driver.find_element(By.XPATH, percent_xpath)
    return play.text, percent.text

plot_element = driver.find_element(By.XPATH, graph_xpath)
actions = ActionChains(driver)
actions.move_to_element(plot_element).perform()

def find_first_play():
    plot_element = driver.find_element(By.XPATH, graph_xpath)
    actions = ActionChains(driver)
    actions.move_to_element(plot_element).perform()
    v = get_vals()
    relevant_text = v[0][0:13]
    cursor_at_first_play = False
    while cursor_at_first_play == False:
        time.sleep(0.1)
        prev_vals = get_vals()
        actions.move_by_offset(-1,0).perform() #move cursor left one pixel
        new_vals = get_vals()
        if new_vals != prev_vals:
            print_vals()
            if new_vals[0][0:13] == "(15:00 - 1st)":
                cursor_at_first_play = True
    print("**********First Play has been reached!*************")

current_play_text = driver.find_element(By.XPATH, "//*[@id='gameFlowPopup-185']/div[3]/p[2]")
print(f'current play: {current_play_text.text}')

print('--')
for i in range(10):
    if i == 0:
        print_vals()
    else:
        time.sleep(0.1)
        #print_vals()
        prev_vals = get_vals()
        actions.move_by_offset(-1,0).perform()
        current_vals = get_vals()
        if current_vals != prev_vals:
            print_vals()
            
print('*')
print('*')
print('*')
print('*')
print('*')
print('')

find_first_play()