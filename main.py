from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from mssql import DataInsertion
import string
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer

app = Flask(__name__)

# Load data from SQL server
review = pd.DataFrame(DataInsertion().query('select * from review'))
business = pd.DataFrame(DataInsertion().query('select * from business'))
business.columns = ['id', 'alias', 'name', 'url', 'eview_count', 'phone', 'distance', 'latitude', 'longitude', 'rating', 'categories', 'transactions']
review.columns = ['review_id', 'text', 'rating','time_created','user_id', 'business_id']
business.dropna(inplace=True)
review.dropna(inplace=True)
review_user = review[['business_id', 'text', 'rating', 'user_id']]

# Define stopwords and punctuation
stop = set(stopwords.words('english'))
punctuation = set(string.punctuation)

# Define function to remove stopwords and punctuation
def remove_stopwords_and_punctuation(text):
    return " ".join([word for word in text.split() if word.lower() not in stop and word not in punctuation])

# Process user and business text data
user_text = review_user[['user_id', 'text']].groupby('user_id').agg(lambda x: " ".join(x))
user_text['text'] = user_text['text'].apply(remove_stopwords_and_punctuation)
business_text = review_user[['business_id', 'text']].groupby('business_id').agg(lambda x: " ".join(x))
business_text['text'] = business_text['text'].apply(remove_stopwords_and_punctuation)

# Create TF-IDF vectors for user and business text data
userid_vectorizer = TfidfVectorizer(tokenizer=WordPunctTokenizer().tokenize, max_features=5000)
userid_vectors = userid_vectorizer.fit_transform(user_text['text'])
businessid_vectorizer = TfidfVectorizer(tokenizer=WordPunctTokenizer().tokenize, max_features=5000)
businessid_vectors = businessid_vectorizer.fit_transform(business_text['text'])

# Create pivot table for user-item ratings
userid_rating_matrix = pd.pivot_table(review_user, values='rating', index=['user_id'], columns=['business_id'])

# Initialize P and Q matrices
P = pd.DataFrame(userid_vectors.toarray(), index=user_text.index, columns=userid_vectorizer.get_feature_names_out())
Q = pd.DataFrame(businessid_vectors.toarray(), index=business_text.index, columns=businessid_vectorizer.get_feature_names_out())

# Define function for matrix factorization
def matrix_factorization(R, P, Q, steps, gamma=0.001, lamda=0.02):
    for i in range(steps):
        for i in R.index:
            for j in R.columns:
                if R.loc[i, j] > 0:
                    eij = R.loc[i, j] - np.dot(P.loc[i], Q.loc[j])
                    P.loc[i] += gamma * (eij * Q.loc[j] - lamda * P.loc[i])
                    Q.loc[j] += gamma * (eij * P.loc[i] - lamda * Q.loc[j])
        e = 0
        for i in R.index:
            for j in R.columns:
                if R.loc[i, j] > 0:
                    e += pow(R.loc[i, j] - np.dot(P.loc[i], Q.loc[j]), 2) + lamda * (pow(np.linalg.norm(P.loc[i]), 2) + pow(np.linalg.norm(Q.loc[j]), 2))
        if e < 0.001:
            break
    print(f"Step: {i}")
from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from mssql import DataInsertion

app = Flask(__name__)

# Load data from SQL server
review = pd.DataFrame(DataInsertion().query('select * from review'))
business = pd.DataFrame(DataInsertion().query('select * from business'))
business.columns = ['id', 'alias', 'name', 'url', 'eview_count', 'phone', 'distance', 'latitude', 'longitude', 'rating', 'categories', 'transactions']
review.columns = ['review_id', 'text', 'rating','time_created','user_id', 'business_id']
business.dropna(inplace=True)
review.dropna(inplace=True)
review_user = review[['business_id', 'text', 'rating', 'user_id']]

# Define stopwords and punctuation
stop = set(stopwords.words('english'))
punctuation = set(string.punctuation)

# Define function to remove stopwords and punctuation
def remove_stopwords_and_punctuation(text):
    return " ".join([word for word in text.split() if word.lower() not in stop and word not in punctuation])

# Process user and business text data
user_text = review_user[['user_id', 'text']].groupby('user_id').agg(lambda x: " ".join(x))
user_text['text'] = user_text['text'].apply(remove_stopwords_and_punctuation)
business_text = review_user[['business_id', 'text']].groupby('business_id').agg(lambda x: " ".join(x))
business_text['text'] = business_text['text'].apply(remove_stopwords_and_punctuation)

# Create TF-IDF vectors for user and business text data
userid_vectorizer = TfidfVectorizer(tokenizer=WordPunctTokenizer().tokenize, max_features=5000)
userid_vectors = userid_vectorizer.fit_transform(user_text['text'])
businessid_vectorizer = TfidfVectorizer(tokenizer=WordPunctTokenizer().tokenize, max_features=5000)
businessid_vectors = businessid_vectorizer.fit_transform(business_text['text'])

# Create pivot table for user-item ratings
userid_rating_matrix = pd.pivot_table(review_user, values='rating', index=['user_id'], columns=['business_id'])

# Initialize P and Q matrices
P = pd.DataFrame(userid_vectors.toarray(), index=user_text.index, columns=userid_vectorizer.get_feature_names_out())
Q = pd.DataFrame(businessid_vectors.toarray(), index=business_text.index, columns=businessid_vectorizer.get_feature_names_out())

# Define function for matrix factorization
def matrix_factorization(R, P, Q, steps, gamma=0.001, lamda=0.02):
    for i in range(steps):
        for i in R.index:
            for j in R.columns:
                if R.loc[i, j] > 0:
                    eij = R.loc[i, j] - np.dot(P.loc[i], Q.loc[j])
                    P.loc[i] += gamma * (eij * Q.loc[j] - lamda * P.loc[i])
                    Q.loc[j] += gamma * (eij * P.loc[i] - lamda * Q.loc[j])
        e = 0
        for i in R.index:
            for j in R.columns:
                if R.loc[i, j] > 0:
                    e += pow(R.loc[i, j] - np.dot(P.loc[i], Q.loc[j]), 2) + lamda * (pow(np.linalg.norm(P.loc[i]), 2) + pow(np.linalg.norm(Q.loc[j]), 2))
        if e < 0.001:
            break
    print(f"Step: {i}")
    return P, Q

#Define Flask app
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
        # Get input text from user
    input_text = request.form['input_text']
    # Process input text
    input_text_df = pd.DataFrame([input_text], columns=['text'])
    input_text_df['text'] = input_text_df['text'].apply(str)
    input_text_df['text'] = input_text_df['text'].apply(lambda x: x.lower())
    input_vector = userid_vectorizer.transform(input_text_df['text'])
    input_v_df = pd.DataFrame(input_vector.toarray(), index=input_text_df.index, columns=userid_vectorizer.get_feature_names_out())
    # Calculate predicted rating for each restaurant
    predictItemRating = pd.DataFrame(np.dot(input_v_df.loc[0], Q.T), index=Q.index, columns=['Rating'])

    # Get top 5 recommendations
    topRecommendations = pd.DataFrame.sort_values(predictItemRating, ['Rating'], ascending=[0])[:5]

    # Get name, rating, and URL for each restaurant
    recommendations = []
    for i in topRecommendations.index:
        restaurant = business.loc[business['id'] == i]
        name = restaurant['name'].values[0]
        rating = restaurant['rating'].values[0]
        url = restaurant['url'].values[0]
        recommendations.append({'name': name, 'rating': rating, 'url': url})

    # Render results page with recommendations
    return render_template('results.html', recommendations=recommendations)
if __name__ == '__main__':
    app.run(debug=True)