import requests
import json

r = requests.get('https://api-v3.mbta.com/lines?sort=long_name')
y = json.dumps(r.text, indent=2)
print(y)