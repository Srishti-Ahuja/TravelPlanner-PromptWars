import requests, json, sys
url_intent = 'http://127.0.0.1:8000/api/intent'
resp = requests.post(url_intent, json={'query':'Plan a trip to Paris'})
print('Intent status:', resp.status_code)
print('Intent body:', resp.text)

url_itin = 'http://127.0.0.1:8000/api/itinerary'
points = [{'name':'A','lat':48.8566,'lng':2.3522},{'name':'B','lat':48.8606,'lng':2.3376}]
resp2 = requests.post(url_itin, json={'points': points})
print('Itinerary status:', resp2.status_code)
print('Itinerary body:', resp2.text)
