'''
function for returning the betting probabilities on each team for a single game
'''
import json
import numpy as np
import requests

def get_game(market_hash = "0xbed7c4f11c0b199ad0cfb89a8a7d1dd7e302f5fb8e9506e54e333e4436af4fcb"):
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