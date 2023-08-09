import pandas as pd
import pypyodbc as odbc
import requests
from config import API_KEY

class DataInsertion:
    def __init__(self):
        self.sql_driver_name = 'SQL SERVER'
        self.sql_server_name = 'Derrick\SQLEXPRESS'
        self.sql_database_name = 'RestaurantRecommendationSystem'
        self.df = pd.DataFrame()
        self.conn = None
        self.cursor = None
        
    def establish_connection(self):
        connection_string = f"""
            DRIVER={{{self.sql_driver_name}}};
            SERVER={self.sql_server_name};
            DATABASE={self.sql_database_name};
            Trust_Connection=yes;
        """
        self.conn = odbc.connect(connection_string, autocommit=True)
        self.cursor = self.conn.cursor()
    
    def close_connection(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()
            
    def query(self, qr):
        self.establish_connection()
        self.cursor.execute(qr)
        result = self.cursor.fetchall()
    #    self.close_connection()
        return result

    def insert_review_to_mssql(self, data):
        self.establish_connection()
        self.df = data
        query = """
        INSERT INTO review (id, text, rating, time_created, user_id, business_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = [(row.id, row.text, row.rating, row.time_created, row.user_id, row.business_id) for row in self.df.itertuples(index=False)]
        self.cursor.executemany(query, params)
        self.close_connection()
    def insert_business_to_mssql(self,data):
        self.establish_connection()
        self.df = data
        query = """
        INSERT INTO business (id, alias, name, url, image_url, review_count, phone, distance, latitude, longitude, rating, categories, transactions) 
        VALUES (?, ?, ?, ?, ?,?, ?, ?, ?, ?,?,?, ?)
        """
        params = [(row.id, row.alias, row.name, row.url, row.image_url, row.review_count, row.phone, row.distance, row.latitude,row.longitude, row.rating, row.categories_str, row.transactions_str) for row in self.df.itertuples(index=False)]
        self.cursor.executemany(query, params)
     #   self.close_connection()

    def change_offset(self, value):
        self.establish_connection()
        query = "update offset_table set offset={}".format(value)
        self.cursor.execute(query)
        

    def clean_review_id(self, id):
        api_get = f'https://api.yelp.com/v3/businesses/{id}/reviews'
        api_key = API_KEY
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(api_get, headers=headers)
        review = pd.json_normalize(response.json()['reviews'])
        review = review.drop(columns=['url','user.profile_url','user.image_url','user.name'])
        review['business_id'] = id
        review = review.rename(columns={'user.id':'user_id'})
        review = review.dropna()
        return review
    

    def get_reviews(self, data):
        business_id = data['id']
        for bid in business_id:
            t = self.clean_review_id(bid)
            self.insert_review_to_mssql(t)


