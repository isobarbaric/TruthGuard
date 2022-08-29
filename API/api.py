
from __main__ import app

from flask import Flask
from flask_restful import Api, Resource
from newspaper import Article

import pandas as pd
import pickle
import json

import os
import sys

# adding extra file path to get accesss to bag of words class
sys.path.append(os.path.abspath(os.getcwd() + "/Pipeline"))

from bag_of_words import BagOfWords

with open('API/model.pkl', 'rb') as file:
    model = pickle.load(file)

def build_predict_dataframe(test_content: str) -> pd.DataFrame:
    with open('Data/model/relevant_words.json') as f:
        relevant_words = json.loads(f.read())
    current_test = BagOfWords(test_content, None)
    cols = {}
    for word in relevant_words:
        cols[word] = [current_test.freq_chart[word] if word in current_test.freq_chart else 0]
    return pd.DataFrame(data = cols)

@app.route('/API/<path:link>', methods=['GET'])
def predict(link):
    current_article = Article(link)

    try:
        current_article.download()
        current_article.parse()

        df = build_predict_dataframe(current_article.text)
    except Exception as e:
        return {'article_link': link, 'error': str(e)}, 400

    prediction_number = model.predict(df)[0]
    if prediction_number == 0:
        prediction = 'conspiracy/pseudoscience'
    else:
        prediction = 'pro-science'

    confidence_level = model.predict_proba(df)[0].tolist()

    confidence_level = {
        'pro-science': confidence_level[1],
        'conspiracy/pseudoscience': confidence_level[0]
    }

    return {'article_link': link, 'prediction': prediction, 'confidence_level': confidence_level}, 200


