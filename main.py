import schedule
import time
from yelp_api import YelpDataRetriever
from data_cleaning import YelpDataProcessor
from mssql import DataInsertion
def run_3min_task():
    # RETRIEVE DATA FROM YELP API + UP TO MONGO
    yelp_retriever = YelpDataRetriever()
    yelp_retriever.retrieve_business()

    # CLEAN DATA
    yelp_processor = YelpDataProcessor()
    yelp_processor.process_data(yelp_retriever.get_business_json())
    business_df_clean = yelp_processor.get_processed_data()

    # UPLOAD TO MSSQL
    DataInsertion().insert_business_to_mssql(business_df_clean)
    DataInsertion().get_reviews(business_df_clean)
    print('run')
run_3min_task()
schedule.every().minute.do(run_3min_task)
while True:
    schedule.run_pending()
    time.sleep(1)
