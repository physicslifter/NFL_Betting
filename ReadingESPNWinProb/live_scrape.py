from selenium import webdriver
from selenium.webdriver.common import keys, by
Keys,  By = keys.Keys(), by.By()
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from games2 import Game, clean_time
import datetime
import time
from matplotlib import pyplot as plt
from matplotlib.figure import Figure 
import pandas as pd
import matplotlib.animation as animation

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
    
    if minute == 'Halftime':
        minute = 0
        quarter = 3
        second = 0
    else:
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

class DriverHandler:
    '''
    For handling driver setup & changing
    '''
    def __init__(self):
        self.s = Service('../chromedriver_win32_107/chromedriver.exe')

    def get_http(self, http_address):
        self.driver = webdriver.Chrome(service=self.s)
        self.driver.get(http_address)

url = "https://www.espn.com/nfl/game/_/gameId/401437854"

def look_for_data(ID):
    game = Game(ID)
    #self.game.d.get_http(url)
    game.go_to_plot()

import json
import numpy as np
import requests

def get_game(market_hash = "0x53f5fc2d98e7c5343a1c08fd38276c82b31c937d177e19637114519bdf5db87b"):
    headers = {"X-Api-Key": "6941d146-b32a-40f6-ae3d-afc7c0f19e50"}
    headers2 = {"marketHashes": [market_hash]}
    json_head = json.dumps(headers2)
    order_req = requests.post("https://api.sx.bet/orders", json=headers2, headers = headers)
    outcome1Odds = []
    outcome2Odds = []
    for i, item in enumerate(order_req.json()['data']):
        print(i, ': ', item['percentageOdds'], item['isMakerBettingOutcomeOne'])
        if item['isMakerBettingOutcomeOne'] == True:
            #favored_team = market['outcomeOneName']
            taker_odds = 1 - int(item['percentageOdds'])/(10**20)
            outcome1Odds.append(taker_odds)
        else:
            #favored_team = market['outcomeTwoName']
            taker_odds = int(item['percentageOdds'])/(10**20)
            outcome2Odds.append(taker_odds)
    #print(f"avg Min bet prob: {np.mean(outcome1Odds)}")
    #print(f"avg NE bet prob: {np.mean(outcome2Odds)}")
    odds = np.mean(outcome1Odds), np.mean(outcome2Odds)
    return odds

#look_for_data(401437854)

def check_started(gameID):
    '''
    returns true if game is live, false if game is not live
    For game you are waiting to start
    '''
    game = Game(gameID)
    try:
        game.go_to_plot()
        #game.find_first_play()
        vals = game.get_vals()
        print(vals)
        return True
    except:
        return False

class LiveGame:
    def __init__(self, ID):
        self.gameID = ID
        self.game = Game(ID)
        self.game.open_page()
        self.home_element = self.game.d.driver.find_element(By.CLASS_NAME, "home")
        self.home = self.home_element.text
        self.away_element = self.game.d.driver.find_element(By.CLASS_NAME, "away")
        self.away = self.away_element.text

    def get_current_game_time(self):
        self.time_element = self.game.d.driver.find_element(By.CLASS_NAME, "game-time")
        self.time = self.time_element.text
        print(self.time)
        self.clean_time = clean_time(self.time)
        return self.clean_time

    def get_current_win_prob(self):
        win_prob_element = self.game.d.driver.find_element(By.CLASS_NAME, "time-info")
        print(win_prob_element.text)
        favored_team = win_prob_element.text[0:3].replace(" ", "")
        win_prob = float(win_prob_element.text[3:-1].replace(" ", ""))
        if favored_team == self.home:
            self.current_home_win_prob = win_prob
            self.current_away_win_prob = 100 - win_prob
        else:
            self.current_home_win_prob = 100 - win_prob
            self.current_away_win_prob = win_prob
        
    def get_and_write_current_data(self):
        self.get_current_win_prob()
        self.get_current_game_time()
        date=datetime.date.today()
        tidy_date = date.strftime('m%d%Y')
        save_file = f"../LiveData/{self.gameID}.csv"
        self.save_file = save_file
        betting_odds = get_game()
        with open(save_file, 'a+') as f:
            f.write(f"{str(datetime.datetime.now())}, {str(self.current_home_win_prob)}, {str(self.current_away_win_prob)}, {betting_odds[0]}, {betting_odds[1]}, {str(self.time)}, {str(self.clean_time)}\n")

    def game_over_check(self):
        self.get_current_win_prob()
        return self.current_home_win_prob == 100 or self.current_away_win_prob == 100

    def poll_current_game(self):
        while self.game_over_check() == False:
            self.get_and_write_current_data()
            time.sleep(1)

    def check_started(self):
        try:
            self.get_current_win_prob()
            return True
        except:
            return False
    def get_current_play_data(self):
        play_element = self.game.d.driver.find_element(By.XPATH, "//*[@id='gameFlowPopup-185']/div[3]/p[2]")

def plot_live_data(gameID):
    fig = Figure()
    axhome = fig.add_subplot(1,2,1)
    axaway = fig.add_subplot(1, 2, 2)

    def animate(i):
        axhome.clear()
        axaway.clear()
        axhome.set_title("Eagles")
        axaway.set_title("Packers")
        data = pd.read_csv(f"../LiveData/{gameID}.csv")
        corrected_odds_data = 1 - data.iloc[:,4].astype(float)
        axhome.scatter(data.iloc[:,6], 100*corrected_odds_data)
        axhome.plot(data.iloc[:, 6], data.iloc[:,2])
        axaway.scatter(data.iloc[:,6], 100*data.iloc[:,3].astype(float))
        axaway.plot(data.iloc[:, 6], data.iloc[:,1])

    ani=animation.FuncAnimation(fig,animate, frames = 100, interval=1000, repeat=True)
    plt.show()
    #ani.save("firstani.gif")



