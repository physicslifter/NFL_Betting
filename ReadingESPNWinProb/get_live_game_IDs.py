from selenium import webdriver
from selenium.webdriver.common import keys, by
Keys,  By = keys.Keys(), by.By()
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service



scoreboard_url = "https://www.espn.com/nfl/scoreboard"


class DriverHandler:
    '''
    For handling driver setup & changing
    '''
    def __init__(self):
        self.s = Service('../chromedriver_win32_107/chromedriver.exe')

    def get_http(self, http_address):
        self.driver = webdriver.Chrome(service=self.s)
        self.driver.get(http_address)


d = DriverHandler()
d.get_http(scoreboard_url)

live_game_class = "ScoreboardScoreCell--in" #in-progress games
upcoming_game_class = "ScoreboardScoreCell--pre" #upcoming games

live_games = d.driver.find_elements(By.CLASS_NAME, live_game_class)
upcoming_games = d.driver.find_elements(By.CLASS_NAME, upcoming_game_class)

live_game_IDs = []
for game in live_games:
    print('===')
    print(type(game))
    print(f'game text: {game.text[0:]}')
    parents = game.find_elements(By.XPATH, "../../../../..")
    print(f'parent text:')
    for parent in parents:
        print(1)
        print(parent.get_attribute('id'))
        live_game_IDs.append(parent.get_attribute('id'))

