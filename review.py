import requests as rq
import pandas as pd 
from config import API_KEY
api_get = 'https://api.yelp.com/v3/businesses/search'
api_key = API_KEY
headers = {"Authorization": f"Bearer {api_key}"}
params = {"location": "OH"}
response = rq.get(api_get, headers=headers, params=params)
print(response.json())