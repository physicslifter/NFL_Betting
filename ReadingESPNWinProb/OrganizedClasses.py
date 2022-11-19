from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import numpy as np
import pdb
from selenium.webdriver.chrome.service import Service

def get_play_history(id:int):
    pass

class Game:
    def __init__(self, game_ID:int):
        self.id = str(game_ID)
        
    def get_play_history(self, save_name:str = ''):
        s = Service('../chromedriver_win32_107/chromedriver.exe')
        driver = webdriver.Chrome(service=s)
        url = "https://www.espn.com/nfl/game/_/gameId/" + self.id
        #pdb.set_trace()
        
        driver.get(url)

        #important/interesting xpaths
        self.most_recent_play_xpath = "//*[@id='gameFlowPopup-185']/div[3]/p[2]" #play data, time, etc
        self.graph_xpath = "//*[@id='gameFlow-graph']/div/div" #The path for the plot play-by-play
        self.percent_xpath = "//*[@id='gameFlowPopup-185']/div[1]/h5"

        def print_vals():
            play = driver.find_element(By.XPATH, self.most_recent_play_xpath)
            percent = driver.find_element(By.XPATH, self.percent_xpath)
            print('================')
            print(f'Win probability: {percent.text}')
            print(f'Most recent play: {play.text[0:12]}')
    
        def get_vals():
            play = driver.find_element(By.XPATH, self.most_recent_play_xpath)
            percent = driver.find_element(By.XPATH, self.percent_xpath)
            return play.text, percent.text

        plot_element = driver.find_element(By.XPATH, self.graph_xpath)
        actions = ActionChains(driver)
        actions.move_to_element(plot_element).perform()

        def find_first_play():
            v = get_vals()
            relevant_text = v[0][0:13]
            cursor_at_first_play = False
            while cursor_at_first_play == False:
                #time.sleep(0.1)
                prev_vals = get_vals()
            actions.move_by_offset(-1,0).perform() #move cursor left one pixel
            print('Moved')
            new_vals = get_vals()
            if new_vals != prev_vals:
                #print_vals()
                if new_vals[0][0:13] == "(15:00 - 1st)":
                    cursor_at_first_play = True
            print("**********First Play has been reached!*************")
            
        find_first_play()
        actions.move_by_offset(-1,0).perform()

        def log_plays():
            v = get_vals()
            cursor_at_end = False
            #times, probabilities = [], []
            data = []
            c=0
            while cursor_at_end == False:
                #time.sleep(0.1)
                prev_vals = get_vals()
                actions.move_by_offset(1,0).perform()
                new_vals = get_vals()
        
                if new_vals[0][0:12] == "(0:00 - 4th)":
                    cursor_at_end = True
        
                if new_vals != prev_vals:
                    #times.append(new_vals[0][1:6])
                    #probabilities.append(new_vals[1])
                    data.append([new_vals[0][1:13], new_vals[1]])
                    #print_vals()
            
                if c==50:
                    #cursor_at_end = True
                    pass    
                c+=1
            
            #print(times, probabilities)
            #return times, probabilities
            print(data)
            return data

        rows = log_plays()

        if save_name == '':
            file_name = save_name + '.csv'
            np.savetxt(file_name,
                   rows,
                   delimiter = ", ",
                   fmt ='% s')
            
        return pd.DataFrame(rows)
        
            
        