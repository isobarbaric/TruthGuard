from typing import Union
import nltk
import string
import pandas as pd
import matplotlib.pyplot as plt

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from dateutil.parser import parse

class BagOfWords:

    def __init__(self, article_texts: Union[pd.DataFrame, str], name: Union[str, None]):
        # declaring instance variables using constructor parameters
        if isinstance(article_texts, pd.DataFrame):
            self.article_texts = article_texts['text'].values.tolist()
        else:
            self.article_texts = article_texts      
        self.name = name

        # declaring additional instance variables
        self.words =  []
        self.freq_chart = dict()

        # method calls
        self.tokenize()
        self.to_lower_case()
        self.clean_data()
        self.remove_stop_words()

        # TODO: normalize seems to be the wrong term here, I mean 'lemmatize', but also review what normalization is just in case
        self.normalize_words()

        self.create_frequency_chart()

        # frequency is only plotted when proper name is provided
        if name:
            self.plot_frequency_chart()

    def tokenize(self):
        if isinstance(self.article_texts, str):
            for word in word_tokenize(self.article_texts):
                self.words.append(word)
        else:
            for article in self.article_texts:
                for word in word_tokenize(article):
                    self.words.append(word)

    def to_lower_case(self):
        for i in range(len(self.words)):
            self.words[i] = self.words[i].lower()

    def clean_data(self):
        noise = ['...', "n't"]
        def is_time_or_date(word):  
            try:
                _ = parse(word)
                return True
            except Exception:
                return False

        def is_link(word):
            suffixes = ['.com', '.org', '.edu', '.gov', '.int', '.co', '.net', '.au', '.us', '.uk', '.ne', 'news']
            for suffix in suffixes:
                if suffix in word:
                    return True
            return False

        for i in range(len(self.words)-1, -1, -1):
            word_to_be_removed = False

            if (len(self.words[i])) <= 2:
                word_to_be_removed = True

            if self.words[i].isnumeric():
                word_to_be_removed = True

            if is_time_or_date(self.words[i]):
                word_to_be_removed = True

            if self.words[i] in noise:
                word_to_be_removed = True

            if is_link(self.words[i]):
                word_to_be_removed = True

            if self.words[i] in [letter for letter in string.ascii_lowercase]:
                word_to_be_removed = True

            if word_to_be_removed:
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
        for word in self.words:
            if word not in self.freq_chart:
                self.freq_chart[word] = 1
            else:
                self.freq_chart[word] += 1

        # sorting in ascending order by value
        self.freq_chart = {word: self.freq_chart[word] for word in sorted(self.freq_chart, key=self.freq_chart.get, reverse=True)}

    def plot_frequency_chart(self):
        words = list(self.freq_chart.keys())[:100]
        frequencies = list(self.freq_chart.values())[:100]

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
