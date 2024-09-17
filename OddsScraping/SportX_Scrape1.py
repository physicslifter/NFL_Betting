'''
First attempt @ scraping data from the SportX API
'''
import requests
import pdb
import json
import numpy as np

#auth = requests.auth.HTTPBasicAuth("X-Api-Key", "6941d146-b32a-40f6-ae3d-afc7c0f19e50")
headers = {"X-Api-Key": "6941d146-b32a-40f6-ae3d-afc7c0f19e50"}

req = requests.get("https://api.sx.bet/markets/active?liveOnly=true", headers = headers)
league_req = requests.get("https://api.sx.bet/leagues", headers = headers)
for i in league_req.json()['data']:
    if i['label'][0] == "N":
        print(f"{i['label']}: {i['leagueId']}")
for market in req.json()['data']['markets']:
    #print(market)
    if market['leagueLabel'] == "NFL" and market['outcomeVoidName'] == "NO_CONTEST":
    #print(f"{market['leagueLabel']}: {market['marketHash']}")
        print(market)
        print('==')
        my_market = market
print(type(req.json()))
my_json = req.json()
for key in my_json.keys():
    print(key)
    
headers2 = {"marketHashes": ["0xbed7c4f11c0b199ad0cfb89a8a7d1dd7e302f5fb8e9506e54e333e4436af4fcb"]}
headers3 = '{"X-Api-Key": "6941d146-b32a-40f6-ae3d-afc7c0f19e50", "marketHashes": ["0x5cd95276caecdeb8dfa48f5e71af5aabd26518bab6ae988099e621bedc62f00c"]}'
json_head = json.dumps(headers2)
order_req = requests.post("https://api.sx.bet/orders", json=headers2, headers = headers)
outcome1Odds = []
outcome2Odds = []
for i, item in enumerate(order_req.json()['data']):
    print(i, ': ', item['percentageOdds'], item['isMakerBettingOutcomeOne'])
    if item['isMakerBettingOutcomeOne'] == True:
        favored_team = my_market['outcomeOneName']
        taker_odds = 1 - int(item['percentageOdds'])/(10**20)
        outcome1Odds.append(taker_odds)
    else:
        favored_team = my_market['outcomeTwoName']
        taker_odds = int(item['percentageOdds'])/(10**20)
        outcome2Odds.append(taker_odds)
print(f"avg Min bet prob: {np.mean(outcome1Odds)}")
print(f"avg NE bet prob: {np.mean(outcome2Odds)}")

pdb.set_trace()
#print(json['data'].keys(), type(json['data']))
#eval(json['data'])