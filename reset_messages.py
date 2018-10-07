import requests
import random

page_id = random.randint(0, 100)
skip_id = random.randint(0, 100)

host = "http://fortunecookieapi.herokuapp.com/v1/fortunes?limit=1&skip=%s&page=%s" % (skip_id, page_id)
r = requests.get(host)
data = r.json()
data = list(data)

for fortune in data:
    message = fortune['message']
    print(message)

