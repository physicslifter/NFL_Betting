from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pdb

url = "https://www.espn.com/nfl/game/_/gameId/401437650"
s = Service('../chromedriver_win32_107/chromedriver.exe')
driver = webdriver.Chrome(service = s)
driver.get(url)

percent = driver.find_element(By.XPATH, "//*[@id='gameFlowPopup-185']/div[1]/h5")
plot_element = driver.find_element(By.XPATH, "//*[@id='gameFlow-graph']/div/div")
actions = ActionChains(driver)
actions.move_to_element(plot_element).perform()
percent1 = percent.text
actions.move_by_offset(-50, 0).perform()
pdb.set_trace()
