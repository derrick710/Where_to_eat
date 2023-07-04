import requests as rq
import pandas as pd
import pymongo
from pymongo import MongoClient, InsertOne

class YelpDataRetriever:
    def __init__(self):
        self.api_url = "https://api.yelp.com/v3/businesses/search"
        self.api_key = "umaP1E2EEpR-tHqS-kOqe5LEztPl3VfMtR97r4HUEYa8M-Wbjpz_qNI_wRnPTeVPOKe987TpJGlZApTHSM-2FgEA6mHqtttOk79zkrOXN-G0jR5POxTEle0nLEXfY3Yx"
        self.headers = {"Authorization": "Bearer {}".format(self.api_key)}
        self.businesses_json = None
        self.business_df = None

    def retrieve_business(self):
        limit = 20
        offset = 0
        total_results = 0
        businesses = []

        while total_results < 100:
            params = {"location": "OH", "limit": limit, "offset": offset}
            try:
                response = rq.get(self.api_url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                retrieved_businesses = data['businesses']
                total_results += len(retrieved_businesses)
                businesses.extend(retrieved_businesses)
                offset += limit
            except rq.exceptions.RequestException as e:
                print("Request failed:", e)

        self.businesses_json = businesses
        self.business_df = pd.DataFrame(businesses)

    def up_to_mongo(self):
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client.RestaurantRecommendationSystem

        collection = db.business
        requesting = [InsertOne(business) for business in self.businesses_json]

        try:
            result = collection.bulk_write(requesting)
            print("Documents inserted:", result.inserted_count)
        except pymongo.errors.BulkWriteError as e:
            print("Bulk write error:", e.details)

        client.close()

    def get_business_df(self):
        return self.business_df

    def get_business_json(self):
        return self.businesses_json