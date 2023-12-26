import gensim.downloader as api
import spacy

class TextProcessor:

    def __init__(self):
        self.embeddings = api.load('word2vec-google-news-300')

        # run python -m spacy download en_core_web_lg first to get access to the model
        self.nlp = spacy.load("en_core_web_lg")

    def preprocess(self, text):
        # print(text)
        # puts all words in lowercase
        text = " ".join([word.lower() for word in text.split()]) 
        article = self.nlp(text)

        # filters out unwanted times, dates, linkes
        only_alpha = [token for token in article if token.is_alpha]
        # removes stop words
        stopwords_filtered = [token for token in only_alpha if not token.is_stop]
        # removes any punctuation
        punct_filtered = [token for token in stopwords_filtered if not token.is_punct]
        # lemmatizes remaining content, all of which should be words
        lemmatized_words = [token.lemma_ for token in punct_filtered]

        return lemmatized_words
    
    def vectorize(self, processed_text: list[str]):
        return self.embeddings.get_mean_vector(processed_text)

    def process(self, text):
        preprocessed_text = self.preprocess(text)
        return self.vectorize(preprocessed_text)