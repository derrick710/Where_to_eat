import requests as rq
import pandas as pd
import pymongo
from pymongo import MongoClient, InsertOne
from mssql import DataInsertion
from config import API_KEY
class YelpDataRetriever:
    def __init__(self):
        self.api_url = "https://api.yelp.com/v3/businesses/search"
        self.api_key = API_KEY
        self.headers = {"Authorization": "Bearer {}".format(self.api_key)}
        self.businesses_json = None
        self.business_df = None

    def retrieve_business(self):
        limit = 5
        offset = DataInsertion().query('select offset from offset_table')[0][0]
        print(f'offset = {offset}')
        total_results = 5
        businesses = []

        while total_results <= 10:
            params = {"location": "OH", "limit": limit, "offset": offset}
            try:
                response = rq.get(self.api_url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                retrieved_businesses = data['businesses']
                total_results += len(retrieved_businesses)
                businesses.extend(retrieved_businesses)
                offset = offset + limit
            except rq.exceptions.RequestException as e:
                print("Request failed:", e)
        DataInsertion().change_offset(offset)
        self.businesses_json = businesses
        self.business_df = pd.DataFrame(businesses)
        return businesses
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
    