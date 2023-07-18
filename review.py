import requests as rq
import pandas as pd 
api_get = f'https://api.yelp.com/v3/businesses/Hp9buzAPpgY0Ioibu2Nj5A/reviews'
api_key = "umaP1E2EEpR-tHqS-kOqe5LEztPl3VfMtR97r4HUEYa8M-Wbjpz_qNI_wRnPTeVPOKe987TpJGlZApTHSM-2FgEA6mHqtttOk79zkrOXN-G0jR5POxTEle0nLEXfY3Yx"
headers = {"Authorization": f"Bearer {api_key}"}
response = rq.get(api_get, headers=headers)
print(response.json())