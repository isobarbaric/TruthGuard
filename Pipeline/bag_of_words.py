
import nltk
import string
import pandas as pd
import matplotlib.pyplot as plt

from typing import Union
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from dateutil.parser import parse

class BagOfWords:

    def __init__(self, article_texts: Union[pd.DataFrame, str], name: Union[str, None]):
        if isinstance(article_texts, pd.DataFrame):
            self.article_texts = article_texts['text'].values.tolist()
        else:
            self.article_texts = article_texts

        self.name = name

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
        self.words = []
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

# from typing import Union
# import string
# import nltk
# import pandas as pd
# import matplotlib.pyplot as plt

# from nltk import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from dateutil.parser import parse

# __author__ = 'isobarbaric'

# class BagOfWords:
#     """Implementation of a modularized Bag of Words model
#     """

#     def __init__(self, article_texts: Union[pd.DataFrame, str], name: Union[str, None]) -> None:
#         """Constructor for BagOfWords class

#         :param article_texts: a collection of either multiple article texts using a pd.DataFrame (with a column appropriately labelled 'text') or a single article (str)
#         :type article_texts: Union[pd.DataFrame, str]
#         :param name: a unique identifier for the collection of article texts being into the current instance
#         :type name: Union[str, None]
#         """
#         # setting the article_texts attribute with a check for the two possible data types outlined in the constructor
#         if isinstance(article_texts, pd.DataFrame):
#             self.article_texts = article_texts['text'].values.tolist()
#         else:
#             self.article_texts = article_texts

#         # setting the name attribute
#         self.name = name

#         # method calls to appropriately create BoW model (address not reassigning and list pass-by-reference thing later)
#         self.words = BagOfWords.tokenize(self.article_texts)
#         BagOfWords.to_lower_case(self.words)
#         BagOfWords.clean_data(self.words)
#         BagOfWords.remove_stop_words(self.words)
#         self.freq_chart = BagOfWords.create_frequency_chart(self.words)
#         BagOfWords.normalize_words(self.words) # TODO: normalize seems to be the wrong term here, I mean 'lemmatize', but also review what normalization is just in case

#         # only plotting the frequency when a distinguishable name is provided
#         if name is not None:
#             BagOfWords.plot_frequency_chart(name, self.freq_chart)

#     @staticmethod
#     def tokenize(corpus: Union[str, list]) -> list:
#         """Performs word tokenization of a corpus

#         :param textual_content: a single article or multiple articles
#         :type textual_content: Union[str, list]
#         :return: individual words occuring in the article(s)
#         :rtype: list
#         """
#         # creating a list to store the words to be found
#         words = []

#         # separating cases for a single article vs multiple articles
#         if isinstance(corpus, str):
#             words = [word for word in word_tokenize(corpus)]
#         else:
#             # looping through the articles and tokenizing each one individually
#             for article in corpus:
#                 for word in word_tokenize(article):
#                     words.append(word)

#         return words

#     @staticmethod
#     def to_lower_case(words: list[str]) -> None:
#         """Converts each word to its lowercase derivative

#         :param words: a vocabulary of words
#         :type words: list[str]
#         """
#         for i, _ in enumerate(words):
#             words[i] = words[i].lower()

#     @staticmethod
#     def clean_data(words: list[str]) -> None:
#         noise = ['...', "n't"]

#         def is_time_or_date(word: str) -> bool:
#             try:
#                 _ = parse(word)
#                 return True
#             except Exception:
#                 return False

#         def is_link(word: str) -> bool:
#             for suffix in ['.com', '.org', '.edu', '.gov', '.int', '.co', '.net', '.au', '.us', '.uk', '.ne', 'news']:
#                 if suffix in word:
#                     return True
#             return False

#         for i in range(len(words)-1, -1, -1):
#             word_to_be_removed = False

#             if (len(words[i])) <= 2:
#                 word_to_be_removed = True

#             if words[i].isnumeric():
#                 word_to_be_removed = True

#             if is_time_or_date(words[i]):
#                 word_to_be_removed = True

#             if words[i] in noise:
#                 word_to_be_removed = True

#             if is_link(words[i]):
#                 word_to_be_removed = True

#             if words[i] in [letter for letter in string.ascii_lowercase]:
#                 word_to_be_removed = True

#             if word_to_be_removed:
#                 words.pop(i)
#                 continue

#             # shave punctation off of beginnings and from the end
#             start_ind, end_ind = -1, -1
#             for j in range(len(words[i])):
#                 if words[i][j] in string.ascii_lowercase or words[i][j].isnumeric():
#                     start_ind = j
#                     break
#             for j in range(len(words[i])-1, -1, -1):
#                 if words[i][j] in string.ascii_lowercase or words[i][j].isnumeric():
#                     end_ind = j
#                     break

#             if (start_ind == 0 and end_ind == len(words[i])-1) or start_ind >= end_ind:
#                 continue

#             words[i] = words[i][start_ind:end_ind+1]

#     @staticmethod
#     def remove_stop_words(words: list[str]) -> None:
#         """Removes stop words

#         :param words: a vocabulary of words
#         :type words: list[str]
#         """
#         for i in range(len(words)-1, -1, -1):
#             if words[i] in stopwords.words('english'):
#                 words.pop(i)

#     @staticmethod
#     def normalize_words(words: list[str]) -> None:
#         def get_part_of_speech(provided_word: str) -> str:
#             _, part_of_speech = nltk.pos_tag([provided_word])[0]
#             if 'NN' in part_of_speech:
#                 return 'n'
#             if 'VB' in part_of_speech:
#                 return 'v'
#             if 'JJ' in part_of_speech:
#                 return 'a'
#             if 'RB' in part_of_speech:
#                 return 'r'
#             return 'n'

#         lemmatizer = WordNetLemmatizer()
#         for i, _ in enumerate(words):
#             words[i] = lemmatizer.lemmatize(words[i], get_part_of_speech(words[i]))

#         # perform some data cleaning on lemmatized words
#         for i in range(len(words)-1, -1, -1):
#             if words[i] in [letter for letter in string.ascii_lowercase]:
#                 words.pop(i)

#     @staticmethod
#     def create_frequency_chart(words: list[str]) -> dict:
#         freq_chart = {}
#         for word in words:
#             if word not in freq_chart:
#                 freq_chart[word] = 1
#             else:
#                 freq_chart[word] += 1
#         # sorting in ascending order by value
#         sorted_freq_chart = sorted(freq_chart, key=freq_chart.get, reverse=True)
#         return {word: freq_chart[word] for word in sorted_freq_chart}

#     @staticmethod
#     def plot_frequency_chart(name: str, freq_chart: dict):
#         words = list(freq_chart.keys())[:100]
#         frequencies = list(freq_chart.values())[:100]

#         plt.figure(figsize=(20, 5))
#         plt.margins(x=0, tight=True)
#         plt.bar(words, frequencies, color ='green')

#         # setting title and labels
#         plt.xlabel("Distinct Words")
#         plt.tick_params(axis='x', which='major', labelsize=9)
#         plt.xticks(rotation = 90)

#         plt.ylabel(f"Frequency of Words in {name}")
#         plt.title("Frequency Chart")

#         # loading the plot
#         plt.show()
