from yelp_api import YelpDataRetriever
from data_cleaning import YelpDataProcessor
from mssql import DataInsertion
import time

while True:
    ### RETRIEVE DATA FROM YELP API + UP TO MONGO
    yelp_retriever = YelpDataRetriever()
    yelp_retriever.retrieve_business()
    # yelp_retriever.up_to_mongo()

    ### CLEAN DATA
    yelp_processor = YelpDataProcessor()
    yelp_processor.process_data(yelp_retriever.get_business_json())
    business_df_clean = yelp_processor.get_processed_data()
    print(business_df_clean)

    ### UPLOAD TO MSSQL
    msinsert = DataInsertion()
    print(business_df_clean['name'])
    DataInsertion().insert_business_to_mssql(business_df_clean)
    DataInsertion().get_reviews(business_df_clean)

    
