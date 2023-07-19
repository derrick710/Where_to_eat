from flask import Flask, request
import pickle
import pandas as pd
from nltk.corpus import stopwords 
import nltk
import string
import numpy as np
import json
import requests

nltk.download('stopwords')

# Load ML model
P, Q, userid_vectorizer = pickle.load(open("./model/yelp_recommendation_model_8.pkl", "rb"))

# Setup text processing
stop = []
for word in stopwords.words('english'):
    s = [char for char in word if char not in string.punctuation]
    stop.append(''.join(s))

api = Flask(__name__)

api_key = "h56sDBVwv3kSJVYzUovbaR-uejvYqdorJL-wvrhJHCytcl0tCw3DDZtIBHLUScuXjZGNSmIs6VV9l96Gr1huG05MOrjSDj5N20UVRx8PQHHa4AjMyKNV0KKYLuTfY3Yx"

# Class to represent a restaurant
class Restaurant:
    def __init__(self, id, name, categories, stars, reviews, image, url):
        self.id = id
        self.name = name
        self.categories = [x['title'] + ", " for x in categories]
        self.stars = stars
        self.reviews = reviews
        self.image = image
        self.url = url
    
    def to_dict(self):
        return {"id": self.id, "name": self.name, "categories": self.categories, "stars": self.stars, "reviews": self.reviews, "image": self.image, "url": self.url}

# Processes inputted text for the ML model
def text_process(mess):
    nopunc = [char for char in mess if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return " ".join([word for word in nopunc.split() if word.lower() not in stop])

# Creates a list of restaurants from a dataframe
def build_results(df):
    restaurants = []
    headers = {"accept": "application/json", "Authorization": "Bearer {}".format(api_key)}
    for id in df.index:
        url = "https://api.yelp.com/v3/businesses/" + id
        response = requests.get(url, headers=headers).json()
        restaurants.append(Restaurant(response['id'],
                                      response['name'],
                                      response['categories'],
                                      str(response['rating']),
                                      str(response['review_count']),
                                      response['image_url'],
                                      response['url']
                                     ))
    return restaurants

@api.route('/search', methods=['POST'])
def generate_recommendations():
    words = request.json["words"]
    test_df= pd.DataFrame([words], columns=['text'])
    test_df['text'] = test_df['text'].apply(text_process)
    test_vectors = userid_vectorizer.transform(test_df['text'])
    test_v_df = pd.DataFrame(test_vectors.toarray(), index=test_df.index, columns=userid_vectorizer.get_feature_names_out())
    predictItemRating=pd.DataFrame(np.dot(test_v_df.loc[0],Q.T),index=Q.index,columns=['Rating'])
    topRecommendations=pd.DataFrame.sort_values(predictItemRating,['Rating'],ascending=[0])[:5]
    return json.dumps({"results": [obj.to_dict() for obj in build_results(topRecommendations)]})