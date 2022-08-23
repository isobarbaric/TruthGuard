from typing import Union
import nltk
import string
import pandas as pd
import matplotlib.pyplot as plt

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from dateutil.parser import parse

__author__ = 'isobarbaric'

class BagOfWords:
    """Implementation of a modularized Bag of Words model
    """

    def __init__(self, article_texts: Union[pd.DataFrame, str], name: Union[str, None]):
        """Constructor for BagOfWords class

        :param article_texts: a collection of either multiple article texts using a pd.DataFrame (with a column appropriately labelled 'text') or a single article (str)
        :type article_texts: Union[pd.DataFrame, str]
        :param name: a unique identifier for the collection of article texts being into the current instance
        :type name: Union[str, None]
        """
        if isinstance(article_texts, pd.DataFrame):
            self.article_texts = article_texts['text'].values.tolist()
        else:
            self.article_texts = article_texts

        self.name = name

        # method calls
        self.words = BagOfWords.tokenize(self.article_texts)
        BagOfWords.to_lower_case(self.words)
        self.clean_data()
        self.remove_stop_words()

        # TODO: normalize seems to be the wrong term here, I mean 'lemmatize', but also review what normalization is just in case
        self.normalize_words()

        self.create_frequency_chart()

        # frequency is only plotted when proper name is provided
        if name:
            self.plot_frequency_chart()

    @staticmethod
    def tokenize(corpus: Union[str, list]) -> list:
        """Performs word tokenization of a corpus

        :param corpus: a single article or multiple articles
        :type textual_content: Union[str, list]
        :return: individual words occuring in the article(s)
        :rtype: list
        """
        words = []
        if isinstance(corpus, str):
            for word in word_tokenize(corpus):
                words.append(word)
        else:
            for article in corpus:
                for word in word_tokenize(article):
                    words.append(word)
        return words

    @staticmethod
    def to_lower_case(words):
        """Converts each word to its lowercase derivative

        :param words: a vocabulary of words
        :type words: list[str]
        """
        for i in range(len(words)):
            words[i] = words[i].lower()

    def clean_data(self):
        noise = ['...', "n't"]
        def is_time_or_date(word):
            try:
                parsed = parse(word)
                return True
            except:
                return False

        def is_link(word):
            suffixes = ['.com', '.org', '.edu', '.gov', '.int', '.co', '.net', '.au', '.us', '.uk', '.ne', 'news']
            for suffix in suffixes:
                if suffix in word:
                    return True
            return False

        for i in range(len(self.words)-1, -1, -1):
            if len(self.words[i]) <= 2 or self.words[i].isnumeric() or is_time_or_date(self.words[i]) or self.words[i] in noise or is_link(self.words[i]) or self.words[i] in [letter for letter in string.ascii_lowercase]:
                self.words.pop(i)
                continue

            # shave punctation off of beginnings and from the end
            start_ind, end_ind = -1, -1
            for j in range(len(self.words[i])):
                if self.words[i][j] in string.ascii_lowercase or self.words[i][j].isnumeric():
                    start_ind = j
                    break
            for j in range(len(self.words[i])-1, -1, -1):
                if self.words[i][j] in string.ascii_lowercase or self.words[i][j].isnumeric():
                    end_ind = j
                    break

            if (start_ind == 0 and end_ind == len(self.words[i])-1) or start_ind >= end_ind:
                continue

            self.words[i] = self.words[i][start_ind:end_ind+1]

    def remove_stop_words(self):
        """Removes stop words

        :param words: a vocabulary of words
        :type words: list[str]
        """
        for i in range(len(self.words)-1, -1, -1):
            if self.words[i] in stopwords.words('english'):
                self.words.pop(i)

    def normalize_words(self):
        def get_part_of_speech(provided_word):
            _, part_of_speech = nltk.pos_tag([provided_word])[0]
            if 'NN' in part_of_speech:
                return 'n'
            if 'VB' in part_of_speech:
                return 'v'
            if 'JJ' in part_of_speech:
                return 'a'
            if 'RB' in part_of_speech:
                return 'r'
            return 'n'

        lemmatizer = WordNetLemmatizer()
        for i in range(len(self.words)):
            self.words[i] = lemmatizer.lemmatize(self.words[i], get_part_of_speech(self.words[i]))

        # perform some data cleaning on lemmatized words
        for i in range(len(self.words)-1, -1, -1):
            if self.words[i] in [letter for letter in string.ascii_lowercase]:
                self.words.pop(i)

    def create_frequency_chart(self):
        self.freqChart = dict()

        for word in self.words:
            if word not in self.freqChart:
                self.freqChart[word] = 1
            else:
                self.freqChart[word] += 1

        # sorting in ascending order by value
        self.freqChart = {word: self.freqChart[word] for word in sorted(self.freqChart, key=self.freqChart.get, reverse=True)}

    def plot_frequency_chart(self):
        words = list(self.freqChart.keys())[:100]
        frequencies = list(self.freqChart.values())[:100]

        plt.figure(figsize=(20, 5))
        plt.margins(x=0, tight=True)
        plt.bar(words, frequencies, color ='green')

        # setting title and labels
        plt.xlabel("Distinct Words")
        plt.tick_params(axis='x', which='major', labelsize=9)
        plt.xticks(rotation = 90)

        plt.ylabel(f"Frequency of Words in {self.name}")
        plt.title("Frequency Chart")

        # loading the plot
        plt.show()
