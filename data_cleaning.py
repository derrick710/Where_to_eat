import numpy as np
import pandas as pd


class YelpDataProcessor:
    def __init__(self):
        self.businesses_json = None
        self.df_flat = None
        self.column_mapping = {
            'coordinates.latitude': 'latitude',
            'coordinates.longitude': 'longitude',
            'location.address1': 'address1',
            'location.address2': 'address2',
            'location.address3': 'address3',
            'location.city': 'city',
            'location.zip_code': 'zip_code',
            'location.country': 'country',
            'location.state': 'state',
            'location.display_address': 'display_address'
        }


    def process_data(self, data):
        self.businesses_json = data
        if self.businesses_json is None:
            raise ValueError("No business data retrieved. Please call retrieve_business() first.")
        
        self.df_flat = pd.json_normalize(self.businesses_json, meta_prefix='b_')
        self.df_flat = self.df_flat.rename(columns=self.column_mapping)
        self.df_flat['is_closed'] = self.df_flat['is_closed'].replace({True: 0, False: 1})
        self.df_flat['categories_list'] = self.df_flat['categories'].apply(lambda x: [category['title'] for category in x] if x else [])
        self.df_flat['categories_str'] = self.df_flat['categories_list'].apply(lambda x: ', '.join(x))
        self.df_flat['transactions_str'] = self.df_flat['transactions'].apply(lambda x: ', '.join(x) if x else '')
        self.df_flat['price_point'] = self.df_flat['price'].apply(lambda x: len(x) if isinstance(x, str) and not pd.isnull(x) else 0)
        self.df_flat = self.df_flat.drop(columns=['price'])
        self.df_flat['address2'] = self.df_flat['address2'].fillna('Not specified')
        self.df_flat['address3'] = self.df_flat['address3'].fillna('Not specified')
        self.df_flat = self.df_flat.drop(columns='is_closed')
        cat_str_arr = []
        tran_str_arr = []
        for row in self.df_flat.itertuples(index=False):
            categories_list = [category['title'] for category in row.categories] if row.categories else []
            categories_str = ', '.join(categories_list)
            transactions_str = ', '.join(row.transactions) if row.transactions else ''
            cat_str_arr.append(categories_str)
            tran_str_arr.append(transactions_str)
        self.df_flat['categories_str'] = cat_str_arr
        self.df_flat['transactions_str'] = tran_str_arr
        self.df_flat.drop(columns=['categories', 'transactions', 'categories_list'], inplace=True)
    def get_processed_data(self):
        if self.df_flat is None:
            raise ValueError("No processed data available. Please call process_data() first.")

        return self.df_flat
