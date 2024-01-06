from flask import Flask, render_template, request
from newspaper import Article
import numpy as np
from text_processor import TextProcessor
import pickle

text_processor = TextProcessor()

# running dummy text to (word embeddings speed up after being used first time)
dummy_text = text_processor.process("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc pulvinar.")

app = Flask(__name__)

# get pickled model to generate predictions
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

def predict(text, type):
    # generating word embeddings for given text
    if type == 'text':
        wb = text_processor.process(text)
    else:
        try:
            curr_article = Article(text) # text is the link here
            curr_article.download(), curr_article.parse()
            article_text = curr_article.text
            wb = text_processor.process(article_text)
        except Exception:
            wb = "error"

    if isinstance(wb, str):
        return {'prediction': "error",
                'probability': {
                                'pro-science': "error",
                                'conspiracy/pseudoscience': "error"
                            }}

    # get probabilities for both labels
    pred_data = model.predict_proba(np.array([wb]))[0]

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

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        link = request.form.get('article-link')
        text = request.form.get('article-text')

        # get model's prediction
        if link is not None:
            prediction = predict(link, type='link')
        else:
            prediction = predict(text, type='text')

        # print(text, link)
        return render_template("result.html", pred = prediction)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    # remove debug=True when deploying
    app.run(debug=True)
