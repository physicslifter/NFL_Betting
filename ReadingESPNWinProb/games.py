from selenium import webdriver
from selenium.webdriver.common import keys, by, action_chains
Keys,  By, ActionChains = keys.Keys(), by.By(), action_chains.ActionChains()
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def clean_datastring(string):
    at_colon = False  
    minute = ''
    second = '' 
    quarter = 0     
    on_second = False
    for i in string:
        if at_colon == False:
            if i == ':':
                at_colon = True
                on_second = True
            else:
                minute += i
        else:
        
            if on_second == True:
                if i != ' ':
                    second += i
                else:
                    on_second = False
            else:
                if i == '1':
                    quarter = 1
                elif i == '2':
                    quarter = 2
                elif i == '3':
                    quarter = 3
                elif i == '4':
                    quarter = 4
                    
    minute = int(minute)
    second = int(second)
    
    return minute, second, quarter

def clean_time(string):
    cleaned_string = clean_datastring(string)
    minute, second, quarter = cleaned_string[0], cleaned_string[1], cleaned_string[2]
    quarter_seconds = (quarter  - 1)*15*60
    minutes_elapsed = 16 - minute
    minute_seconds = minutes_elapsed*60
    seconds_elapsed = 60 - second
    total_seconds_elapsed = quarter_seconds+minute_seconds+seconds_elapsed
    return total_seconds_elapsed

class StringCleaner:
    '''
    For cleaning string data scraped from ESPN.com
    '''
    def __init__(self, raw_string):
        self.string = raw_string
    def clean_datastring(self):
        at_colon = False  
        minute = ''
        second = '' 
        quarter = 0     
        on_second = False
        for i in self.string:
            if at_colon == False:
                if i == ':':
                    at_colon = True
                    on_second = True
                else:
                    minute += i
            else:
                if on_second == True:
                    if i != ' ':
                        second += i
                    else:
                        on_second = False
                else:
                    if i == '1':
                        quarter = 1
                    elif i == '2':
                        quarter = 2
                    elif i == '3':
                        quarter = 3
                    elif i == '4':
                        quarter = 4         
        minute = int(minute)
        second = int(second)
        self.quarter, self.minute, self.second = quarter, minute, second
        return minute, second, quarter

    def clean_time(self):
        quarter_seconds = (self.quarter  - 1)*15*60
        minutes_elapsed = 16 - self.minute
        minute_seconds = minutes_elapsed*60
        seconds_elapsed = 60 - self.second
        total_seconds_elapsed = quarter_seconds+minute_seconds+seconds_elapsed
        return total_seconds_elapsed

    def get_seconds_elapsed(self):
        self.clean_datastring()
        seconds = self.clean_time()
        return seconds

class DriverHandler:
    '''
    For handling driver setup & changing
    '''
    def __init__(self):
        self.s = Service('../chromedriver_win32_107/chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.s)

    def get_http(self, http_address):
        self.driver.get(http_address)

class Game:
    def __init__(self, ID):
        self.d = DriverHandler()
        desired_http = 'https://www.espn.com/nfl/game/_/gameId/' + str(ID)
        self.d.get_http(desired_http)
        #important/interesting xpaths
        self.most_recent_play_xpath = "//*[@id='gameFlowPopup-185']/div[3]/p[2]" #play data, time, etc
        self.graph_xpath = "//*[@id='gameFlow-graph']/div/div" #The path for the plot play-by-play
        self.percent_xpath = "//*[@id='gameFlowPopup-185']/div[1]/h5"
        self.game_date_xpath = "//*[@id='gamepackage-game-information']/article/div/div[1]/div/div[1]/span/span[2]"
        away_path = "//*[@id='linescore']/tbody/tr[1]/td[1]"
        home_path = "//*[@id='linescore']/tbody/tr[2]/td[1]"
        #Getting relevant elements
        self.home = self.d.driver.find_element(By.XPATH, self.home_path).text
        self.away = self.d.driver.find_element(By.XPATH, self.away_path).text
    
    def get_vals(self):
        play = self.d.driver.find_element(By.XPATH, self.most_recent_play_xpath)
        percent = self.d.driver.find_element(By.XPATH, self.d.percent_xpath)
        favored_team = percent.text[0:3].replace(" ","")
        if favored_team == self.home:
            win_prob = 100 - float(percent.text[3:-1].replace(" ", ""))
        else:
            win_prob = float(percent.text[4:-1].replace(" ", ""))
        return play.text, percent.text, win_prob

    def go_to_plot(self):
        plot_element = self.d.driver.find_element(By.XPATH, self.graph_xpath)
        self.actions = ActionChains(self.d.driver)
        self.actions.move_to_element(plot_element).perform()

    def find_first_play(self):
        v = self.get_vals()
        relevant_text = v[0][0:13]
        cursor_at_first_play = False
        while cursor_at_first_play == False:
            #time.sleep(0.1)
            prev_vals = self.get_vals()
            print(prev_vals)
            self.actions.move_by_offset(-1,0).perform() #move cursor left one pixel
            new_vals = self.get_vals()
            if new_vals != prev_vals:
                if new_vals[0][0:13] == "(15:00 - 1st)":
                    cursor_at_first_play = True
        print("**********First Play has been reached!*************")
    
    def log_plays(self):
        v = self.get_vals()
        cursor_at_end = False
        data = []
        c=0
        while cursor_at_end == False:
            prev_vals = self.get_vals()
            self.actions.move_by_offset(1,0).perform()
            new_vals = self.get_vals()
            
            if new_vals[0][0:12] == "(0:00 - 4th)":
                cursor_at_end = True
        
            if new_vals != prev_vals:
                favored_team = new_vals[1][0:3]            
                if favored_team == self.home:
                    win_prob = 100 - float(new_vals[1][4:-1])
                else:
                    win_prob = float(new_vals[1][4:-1])
                data.append([new_vals[0][1:13], new_vals[1], clean_time(new_vals[0][1:13]), new_vals[2]])
            print(new_vals)

            if c==50:
            #cursor_at_end = True
                pass
            c+=1  
        self.data = data
        return data

    def get_date(self):
        date = self.d.driver.find_element(By.XPATH, self.game_date_xpath)
        self.tight_date = date.replace(" ", "").replace(",","")
        self.pretty_date = date

    def save_data(self):
        save_name = f'../Data/{self.home}_vs_{self.away}_{self.tight_date}.csv'
        win_pct_name = f'{self.away}_win_pct'
        df = pd.DataFrame(self.data, columns=["raw_time", "raw_win_pct", "clean_time", win_pct_name])
        df.to_csv(save_name)

    def plot_results(self, save_name = ''):
        plt.suptitle(f'{self.home} vs. {self.away} | {self.pretty_date}')
        plt.xlabel('Game Time (seconds)')
        plt.ylabel(f'{self.home} Win Probability (%)')
        if save_name != '':
            try:
                plt.savefig(save_name)
            except:
                print('WARNING: Plot not saved')
        plt.show()

    def get_play_history(self, plot:bool = True, save_name:str = ''):
        self.go_to_plot()
        self.find_first_play()
        self.get_date()
        self.actions.move_by_offset(-1,0).perform()
        self.log_plays()
        self.save_data()
        if plot == True:
            self.plot_results(save_name)
        

        

    

    

