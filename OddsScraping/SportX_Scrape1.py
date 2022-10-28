'''
First attempt @ scraping data from the SportX API
'''
import requests

#auth = requests.auth.HTTPBasicAuth("X-Api-Key", "6941d146-b32a-40f6-ae3d-afc7c0f19e50")
headers = {"X-Api-Key": "6941d146-b32a-40f6-ae3d-afc7c0f19e50"}
req = requests.post("https://api.sx.bet/trades", headers = headers)
print(type(req.json()))
json = req.json()
for key in json.keys():
    print(key)
    
print(json['data'].keys(), type(json['data']))
eval(json['data'])