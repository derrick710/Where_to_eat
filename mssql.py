import pandas as pd
import pypyodbc as odbc

class DataInsertion:
    def __init__(self):
        self.sql_driver_name = 'SQL SERVER'
        self.sql_server_name = 'Derrick\SQLEXPRESS'
        self.sql_database_name = 'RestaurantRecommendationSystem'
        self.df = pd.DataFrame()

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
            #    address2, address3, city, zip_code, country, state, display_address, categories_str, transactions_str, price_point, rating)
            # phone, display_phone, distance, latitude, longitude, address1)
            cursor.execute("UPDATE business SET name = ?  where id = ?" ,(row.name, row.id))


            #row.phone, row.display_phone, row.distance, row.latitude,
            #row.longitude, row.address1, row.address2, row.address3, row.city, row.zip_code, row.country, row.state,
            #row.display_address, row.categories_str, row.transactions_str, row.price_point, row.rating
        

    


        conn.close()
 