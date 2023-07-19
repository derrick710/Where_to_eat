from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer
from mssql import DataInsertion
import string
import pandas as pd

review = pd.DataFrame(DataInsertion().query('select * from review'))
business =  pd.DataFrame(DataInsertion().query('select * from business'))
review.to_csv('review_snap.csv', header=True)
business.to_csv('business_snap.csv', header = True)

#user_re = pd.read_csv('user_review.csv')


