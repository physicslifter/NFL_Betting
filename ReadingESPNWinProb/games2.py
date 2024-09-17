from selenium import webdriver
from selenium.webdriver.common import keys, by
Keys,  By = keys.Keys(), by.By()
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import datetime
import pdb
import os

def check_data(csv_file:str):
    try:
        a = pd.read_csv(csv_file)
        has_no_gap =  (a.clean_time.values[-1] - a.clean_time.values[-2]) < 100 #if true, less than 100 seconds between last 2 plays, otherwise over 100 seconds between last 2 plays
        has_file = has_no_gap and ((a[a.keys()[-1]].values[-1] == 100) or a[a.keys()[-1]].values[-1] == 0)
    except:
        has_file = False
    return has_file

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
                elif i == 'O':
                    quarter = 5
                    
    minute = int(minute)
    second = int(second)
    
    return minute, second, quarter

def clean_time(string):
    cleaned_string = clean_datastring(string)
    minute, second, quarter = cleaned_string[0], cleaned_string[1], cleaned_string[2]
    quarter_seconds = (quarter  - 1)*15*60
    #quarter_seconds = 3600
    minutes_elapsed = 16 - minute
    minute_seconds = minutes_elapsed*60
    seconds_elapsed = 60 - second
    total_seconds_elapsed = quarter_seconds+minute_seconds+seconds_elapsed
    return total_seconds_elapsed - 120

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

    def get_http(self, http_address):
        self.driver = webdriver.Chrome(service=self.s)
        self.driver.get(http_address)

class Game:
    def __init__(self, ID):
        self.ID = ID
        self.d = DriverHandler()
        #important/interesting xpaths
        self.most_recent_play_xpath = "//*[@id='gameFlowPopup-185']/div[3]/p[2]" #play data, time, etc
        self.graph_xpath = "//*[@id='gameFlow-graph']/div/div" #The path for the plot play-by-play
        self.percent_xpath = "//*[@id='gameFlowPopup-185']/div[1]/h5"
        self.game_date_xpath = "//*[@id='gamepackage-game-information']/article/div/div[1]/div/div[1]/span/span[2]"
        self.away_path = "//*[@id='linescore']/tbody/tr[1]/td[1]"
        self.home_path = "//*[@id='linescore']/tbody/tr[2]/td[1]"
    
    def get_vals(self):
        play = self.d.driver.find_element(By.XPATH, self.most_recent_play_xpath)
        percent = self.d.driver.find_element(By.XPATH, self.percent_xpath)
        if percent.text.replace(" ", "") == "TIE":
            #game is either going to OT, or has ended in a tie
            win_prob = float(50)
        else:
            favored_team = percent.text[0:3].replace(" ","")
            if favored_team == self.home:
                win_prob = 100 - float(percent.text[3:-1].replace(" ", ""))
            else:
                win_prob = float(percent.text[3:-1].replace(" ", ""))
    
        return play.text, percent.text, win_prob

    def open_page(self):
        desired_http = 'https://www.espn.com/nfl/game/_/gameId/' + str(self.ID)
        self.d.get_http(desired_http)

    def close_page(self):
        self.d.driver.quit()

    def go_to_plot(self):
        #desired_http = 'https://www.espn.com/nfl/game/_/gameId/' + str(self.ID)
        #self.d.get_http(desired_http)
        plot_element = self.d.driver.find_element(By.XPATH, self.graph_xpath)
        self.actions = ActionChains(self.d.driver)
        self.actions.move_to_element(plot_element).perform()
        #self.d.driver.close()

    def find_first_play(self):
        v = self.get_vals()
        relevant_text = v[0][0:13]
        cursor_at_first_play = False
        #pdb.set_trace()
        while cursor_at_first_play == False:
            #time.sleep(0.1)
            prev_vals = self.get_vals()
            print(prev_vals)
            self.actions.move_by_offset(-1,0).perform() #move cursor left one pixel
            new_vals = self.get_vals()
            if new_vals != prev_vals:
                if self.ID == 400874522:
                    if new_vals[0][0:13] == "(14:56 - 1st)":
                        cursor_at_first_play = True
                else:
                    if new_vals[0][0:13] == "(15:00 - 1st)":
                        cursor_at_first_play = True
        print("**********First Play has been reached!*************")
    
    def log_plays(self):
        v = self.get_vals()
        cursor_at_end = False
        data = []
        c=0
        consecutive_unchanged = 0
        while cursor_at_end == False:
            prev_vals = self.get_vals()
            self.actions.move_by_offset(1,0).perform()
            new_vals = self.get_vals()

            if prev_vals == new_vals:
                consecutive_unchanged += 1
            else:
                consecutive_unchanged = 0
            
            if new_vals[0][0:12] == "(0:00 - 4th)":
                if new_vals[1] != 'TIE':
                    cursor_at_end = True
            
            if consecutive_unchanged == 30:
                cursor_at_end = True
        
            if new_vals != prev_vals:
                data.append([new_vals[0][1:13], new_vals[1], clean_time(new_vals[0][1:13]), new_vals[2]])
            print(f'new vals: {new_vals} | prev vals: {prev_vals} | at_end: {cursor_at_end}')
            #print(f'prev vals: {prev_vals}')

            if c==50:
            #cursor_at_end = True
                pass
            c+=1  
        self.data = data
        return data

    def get_date(self):
        timestamp = self.d.driver.find_element(By.CLASS_NAME, "timestamp")
        stamptext = timestamp.text
        print(stamptext)
        if stamptext[-1] == 'd':
            num_days_ago = int(stamptext[0])
            date = datetime.date.today() - datetime.timedelta(num_days_ago)
            self.tight_date = date.strftime('%m%d%Y')
            self.pretty_date = date.strftime('%m/%d/%Y')

        else:
            date = self.d.driver.find_element(By.CLASS_NAME, "date")
            #pdb.set_trace()
            self.tight_date = date.text.replace(" ", "").replace(",","").replace("/", "")
            self.pretty_date = date.text

    def save_data(self, save_name = None):
        if save_name == None: 
            save_name = f'../Data/{self.home}_vs_{self.away}_{self.tight_date}.csv'
        win_pct_name = f'{self.away}_win_pct'
        self.df = pd.DataFrame(self.data, columns=["raw_time", "raw_win_pct", "clean_time", win_pct_name])
        self.df.to_csv(save_name)

    def get_game_info(self):
        desired_http = 'https://www.espn.com/nfl/game/_/gameId/' + str(self.ID)
        self.d.get_http(desired_http)
        self.home = self.d.driver.find_element(By.XPATH, self.home_path).text
        self.away = self.d.driver.find_element(By.XPATH, self.away_path).text
        self.get_date()
        has_data = True
        if self.d.driver.find_element(By.CLASS_NAME, "content") == "Data is currently unavailable.":
            has_data = False
        self.d.driver.close()
        return has_data

    def plot_results(self, save_name = ''):
        plt.suptitle(f'{self.home} vs. {self.away} | {self.pretty_date}')
        plt.xlabel('Game Time (seconds)')
        plt.ylabel(f'{self.away} Win Probability (%)')
        win_pct_name = f'{self.away}_win_pct'
        plt.plot(self.df['clean_time'], self.df[win_pct_name])
        if save_name != '':
            try:
                plt.savefig(save_name)
            except:
                print('WARNING: Plot not saved')
        plt.close()
        #plt.show()
        #time.sleep(5)
        #plt.close()

    def get_play_history(self, plot:bool = True, save:bool = True, save_name = None):
        success = True
        complete = False
        count = 0
        desired_http = 'https://www.espn.com/nfl/game/_/gameId/' + str(self.ID)
        self.d.get_http(desired_http)
        self.home = self.d.driver.find_element(By.XPATH, self.home_path).text
        self.away = self.d.driver.find_element(By.XPATH, self.away_path).text
        self.get_date()
        if save_name == None:
            complete = check_data(f'../Data/{self.home}_vs_{self.away}_{self.tight_date}.csv')
        else:
            complete = check_data(save_name)
        self.d.driver.close()
        while complete == False:
            desired_http = 'https://www.espn.com/nfl/game/_/gameId/' + str(self.ID)
            self.d.get_http(desired_http)
            self.home = self.d.driver.find_element(By.XPATH, self.home_path).text
            self.away = self.d.driver.find_element(By.XPATH, self.away_path).text
            self.go_to_plot()
            self.find_first_play()
            self.get_date()
            self.actions.move_by_offset(-1,0).perform()
            self.log_plays()
            self.save_data(save_name = save_name) 
            if plot == True:
                save_name = f'../Plots/{self.home}_vs_{self.away}_{self.tight_date}.png'
                self.plot_results(save_name)
            self.d.driver.close()
            if save_name == None:
                complete = check_data(f'../Data/{self.home}_vs_{self.away}_{self.tight_date}.csv')
            else:
                complete = check_data(save_name)
            count += 1
            if complete == False and count == 5:
                print('Failed to retrieve data')
                complete = True
                success = False
        return success

class GamesOfWeek:
    def __init__(self, week, year):
        self.week = week
        self.year = year
        self.d = DriverHandler()
        self.week_url = f"https://www.espn.com/nfl/scoreboard/_/week/{week}/year/{year}/seasontype/2"
    def get_IDs(self):
        self.d.get_http(self.week_url)
        elements = self.d.driver.find_elements(By.CLASS_NAME, "Scoreboard")
        self.IDs = []
        for element in elements:
            self.IDs.append(element.get_attribute("id"))
        self.d.driver.quit()
        return self.IDs
    def get_data(self, results_file = 'scrape_results.txt'):
        results = []
        for ID in self.IDs:
            self.game = Game(int(ID))
            has_data = self.game.get_game_info()
            if has_data == True: #if there is no data, then don't worry about the game
                try:
                    #check if the folder exists and if not make it
                    if os.path.exists(f'../Data/{self.year}/{self.week}') != True:
                        os.makedirs(f'../Data/{self.year}/{self.week}')
                    save_name = f'../Data/{self.year}/{self.week}/{self.game.home}_vs_{self.game.away}_{self.game.tight_date}.csv'
                    self.game.get_play_history(save_name = save_name)
                    results.append(1)
                except:
                    results.append(0)
        print(results)
        with open (results_file, 'a+') as f:
            f.write(" \n")
            f.write(" \n")
            f.write("=================")
            f.write("\n")
            f.write("\n")
            f.write(str(results))
            f.write("\n")

class LiveScoreboard:
    def __init__(self, ID):
        self.ID = ID
        self.d = DriverHandler()
        self.scoreboardURL = "https://www.espn.com/nfl/scoreboard"
        self.live_game_class = "ScoreboardScoreCell--in" #in-progress games
        self.upcoming_game_class = "ScoreboardScoreCell--pre" #upcoming games
    
    def get_live_games(self):
        self.live_games = self.d.driver.find_elements(By.CLASS_NAME, self.live_game_class)

    def get_live_games(self):
        self.upcoming_games = self.d.driver.find_elements(By.CLASS_NAME, self.upcoming_game_class)  

    def get_live_IDs(self):
        self.d.get_http(self.scoreboardURL)
        self.get_live_games()
        self.live_game_IDs = []
        for game in self.live_games:
            parents = game.find_elements(By.XPATH, "../../../../..")
            for parent in parents:
                self.live_game_IDs.append(parent.get_attribute('id'))

class LiveGame:
    def __init__(self, ID):
        self.ID = ID
        self.d = DriverHandler()
        #important/interesting xpaths
        self.most_recent_play_xpath = "//*[@id='gameFlowPopup-185']/div[3]/p[2]" #play data, time, etc
        self.graph_xpath = "//*[@id='gameFlow-graph']/div/div" #The path for the plot play-by-play
        self.percent_xpath = "//*[@id='gameFlowPopup-185']/div[1]/h5"
        self.game_date_xpath = "//*[@id='gamepackage-game-information']/article/div/div[1]/div/div[1]/span/span[2]"
        self.away_path = "//*[@id='linescore']/tbody/tr[1]/td[1]"
        self.home_path = "//*[@id='linescore']/tbody/tr[2]/td[1]"