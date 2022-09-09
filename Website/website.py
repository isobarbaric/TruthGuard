
from distutils.command.build import build
from flask import render_template, request, Blueprint

import json
import sys
import os
import requests
import pandas as pd
import pickle

# adding extra file path to get accesss to bag of words class
sys.path.append(os.path.abspath(os.getcwd() + "/ML Pipeline"))

from bag_of_words import BagOfWords

website_blueprint = Blueprint(
    'website',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/home-static'
)

def build_predict_dataframe(text_content):
    with open('ML Pipeline/Data/model/relevant_words.json') as f:
        relevant_words = json.loads(f.read())

    current_test = BagOfWords(text_content, None)

    cols = {}
    for word in relevant_words:
        cols[word] = [current_test.freq_chart[word] if word in current_test.freq_chart else 0]

    data_set = pd.DataFrame(data = cols)

    return data_set

with open('API/model.pkl', 'rb') as file:
    model = pickle.load(file)

def predict(article_body):
    df = build_predict_dataframe(article_body)

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

    return {'prediction': prediction,
            'confidence_level': confidence_level}

@website_blueprint.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        article_link = request.form.get('article-link')
        article_body = request.form.get('article-text')

        print(article_body)
        print(article_link)

        prediction = None

        if article_link is not None:
            try:
                api_response = requests.get(f'http://covid19-classifier-app.herokuapp.com/API/{article_link}')
                prediction = api_response.json()
            except Exception as e:
                prediction = e
        elif article_body is not None:
            # construct data in some way as the api response
            prediction = predict(article_body)

        return render_template("result.html", pred = prediction)
    else:
        return render_template('index.html')