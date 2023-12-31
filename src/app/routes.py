import os
import sys
from flask import render_template, request, Blueprint
import numpy as np
import pickle

# fix file path stuff when file directory stuff is restructured
# adding extra file path to get accesss to text processor class
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)

print("Loading text processor...")

from src.model.text_processor import TextProcessor
text_processor = TextProcessor()
dummy_text = text_processor.process("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc pulvinar.")

print("...loaded text processor")

website_blueprint = Blueprint(
    'website',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/home-static'
)

with open('data/model/model.pkl', 'rb') as file:
    model = pickle.load(file)

def generate_pred(text):
    # generating word embeddings for given text
    wb = text_processor.process(text)

    # get probabilities for both labels
    pred = model.predict_proba(np.array([wb]))[0]

    return pred

def predict(text):
    pred_data = generate_pred(text)

    if pred_data[0] >= pred_data[1]:
        prediction = 'conspiracy/pseudoscience'
    else:
        prediction = 'pro-science'

    probability = {
        'pro-science': round(pred_data[1]*100, 2),
        'conspiracy/pseudoscience': round(pred_data[0]*100, 2)
    }

    return {'prediction': prediction,
            'probability': probability}

@website_blueprint.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form.get('article-text')

        prediction = predict(text)
        print(prediction)

        return render_template("result.html", pred = prediction)
    else:
        return render_template('index.html')
