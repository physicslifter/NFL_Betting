import requests
import pdb

headers = {"X-Api-Key": "6941d146-b32a-40f6-ae3d-afc7c0f19e50"}

def print_live_markets():
    req = requests.get("https://api.sx.bet/markets/active?liveOnly=true", headers = headers)
    print(req.json())
    return req.json()

class TotalContest:
    def __init__(self, game_dict:dict):
        self.dict = game_dict
        '''
        team one name is the home team
        '''
        self.home = game_dict['teamOneName']
        self.away = game_dict['teamTwoName']
        self.marketHash = game_dict['marketHash']
        self.line = game_dict['line']

class SpreadContest:
    def __init__(self, game_dict:dict):
        self.dict = game_dict
        '''
        team one name is the home team
        '''
        self.home = game_dict['teamOneName']
        self.away = game_dict['teamTwoName']
        self.marketHash = game_dict['marketHash']
        self.line = game_dict['line']

def get_live_games(league:str="NFL", straight_up:bool=True, spread:bool=True, total:bool=True):
    more_requests = True
    req = requests.get("https://api.sx.bet/markets/active?pageSize=50", headers = headers)
    markets = req.json()['data']['markets']
    while more_requests == True:
        try:
            print("trying...")
            pagkey = req.json()['data']['nextKey']
            print("========================")
            print(pagkey)
            print("=======================")
            req = requests.get(f"https://api.sx.bet/markets/active?paginationKey={pagkey}", headers = headers)
            for market in req.json()['data']['markets']:
                markets.append(market)
        except:
            more_requests = False
    moneyline_contests = []
    total_contests = []
    spread_contests = []
    for i, market in enumerate(markets):
        print(i, market)
        print()
        #pdb.set_trace()
        if market['leagueLabel'] == league:
            
            if straight_up==True:
                if market['outcomeVoidName'] == "NO_CONTEST":
                    moneyline_contests.append(market)
            elif spread ==True:
                if market['outcomeVoidName'] == "NO_GAME_OR_EVEN":
                    if market['outcomeOneName'][0:4] == "Over" or market['outcomeOneName'][0:4] == "Unde":
                        total_contests.append(market)
                    else:
                        spread_contests.append(market)
    return moneyline_contests, spread_contests, total_contests, req

def get_game_bets(marketHashList:list):
    '''
    takes one or several market hashes
    returns orders associated with these hashes
    '''
    market_hash_header = {"marketHashes": marketHashList}
    order_req = requests.post("https://api.sx.bet/orders", json = market_hash_header)
    return order_req.json()['data']



