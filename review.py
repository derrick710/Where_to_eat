import requests as rq
import pandas as pd 
api_get = 'https://api.yelp.com/v3/businesses/search'
api_key = "eWFcY2ZPmejkMzgpI0-yGVkiGX_Tq0BHCyxH4HH-NJCNsYk1MBRx3x0EfPmMlwbcTDjxG9llau4i-lzcdQCVr9355FOasrodfVJ0fA4Qujd_lIMW0tCTveKHLYW3ZHYx"
headers = {"Authorization": f"Bearer {api_key}"}
params = {"location": "OH"}
response = rq.get(api_get, headers=headers, params=params)
print(response.json())