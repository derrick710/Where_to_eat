import pandas as pd
import pypyodbc as odbc

class DataInsertion:
    def __init__(self):
        self.sql_driver_name = 'SQL SERVER'
        self.sql_server_name = 'Derrick\SQLEXPRESS'
        self.sql_database_name = 'RestaurantRecommendationSystem'
        self.df = None

    def insert_data_to_mssql(self, data):
        # Establish connection to SQL Server
        connection_string = f"""
            DRIVER={{{self.sql_driver_name}}};
            SERVER={self.sql_server_name};
            DATABASE={self.sql_database_name};
            Trust_Connection=yes;
        """
        conn = odbc.connect(connection_string, autocommit=True)
        cursor = conn.cursor()
        self.df = data
        # Insert data into MSSQL Business table
        for row in self.df.itertuples(index=False):
            categories_list = [category['title'] for category in row.categories] if row.categories else []
            categories_str = ', '.join(categories_list)
            transactions_str = ', '.join(row.transactions) if row.transactions else ''
            """
            cursor.execute(
                INSERT INTO business
                (id, alias, name, image_url, url, review_count, rating,
                price, phone, display_phone, distance, latitude, longitude, address1,
                address2, address3, city, zip_code, country, state, display_address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?, ?)
                ,
                row.id, row.alias, row.name, row.image_url, row.url, row.review_count, categories_str,
                row.rating, transactions_str, row.price, row.phone, row.display_phone, row.distance, row.latitude,
                row.longitude, row.address1, row.address2, row.address3, row.city, row.zip_code, row.country, row.state,
                row.display_address
            )
            """

        conn.close()
 