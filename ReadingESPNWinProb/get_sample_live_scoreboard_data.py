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

print('Live Games:')
for game in live_games:
    print(f'    {game.text}')
    for c, line in enumerate(game.text):
        print(c)

with open("sample_live_game_scoreboard_text.txt", 'a+') as f:
    f.write("sample live game text")
    f.write(game.text.strip("\n"))
    f.write("\n")

print('')
print('')
print('')
print('')
print('====================')
print('')
print('')
print('')
print('')
print('Upcoming Games:')
for game in upcoming_games:
    print(f'    {game.text.strip()}')
    for c, line in enumerate(game.text):
        print(c)

with open("sample_live_game_scoreboard_text.txt", 'a+') as f:
    f.write(" \n")
    f.write(" \n")
    f.write("=================")
    f.write("\n")
    f.write("\n")
    f.write("sample upcoming game text")
    f.write(game.text)
    f.write("\n")

