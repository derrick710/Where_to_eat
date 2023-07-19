import requests as rq
import pandas as pd 
api_get = f'https://api.yelp.com/v3/businesses/Hp9buzAPpgY0Ioibu2Nj5A/reviews'
api_key = "DeH-dtAQzE9G3tRLohvs62uNUQdHD2XPvlR_qiAbbvkjnNSnqkr-eciC71OatrD0RDi7mxutXq_GOZA33C5GexqO4wgoHZEQva2GaD-deAj0OuWTHVCqOV1fWui2ZHYx"
headers = {"Authorization": f"Bearer {api_key}"}
response = rq.get(api_get, headers=headers)
print(response.json())