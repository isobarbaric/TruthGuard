from typing import Union
import string
import nltk
import pandas as pd
import matplotlib.pyplot as plt

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from dateutil.parser import parse

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

class BagOfWords:
    """Implementation of a modular Bag of Words model
    """

    __author__ = 'isobarbaric'
    __version_info__ = (1, 0, 0)
    __version__ = '.'.join(str(k) for k in __version_info__)

    def __init__(self, article_texts: Union[pd.DataFrame, str], name: Union[str, None]) -> None:
        """Constructor for BagOfWords class

        :param article_texts: a collection of either multiple article texts using a pd.DataFrame (with a column appropriately labelled 'text') or a single article (str)
        :type article_texts: Union[pd.DataFrame, str]
        :param name: a unique identifier for the collection of article texts being into the current instance
        :type name: Union[str, None]
        """

        # setting the article_texts attribute with a check for the two possible data types outlined in the constructor
        if isinstance(article_texts, pd.DataFrame):
            self.article_texts = article_texts['text'].values.tolist()
        else:
            self.article_texts = article_texts

        # setting the name attribute
        self.name = name

        # method calls to appropriately create BoW model (address not reassigning and list pass-by-reference thing later)
        self.words = BagOfWords.tokenize(self.article_texts)
        BagOfWords.to_lower_case(self.words)
        BagOfWords.clean_data(self.words)
        BagOfWords.remove_stop_words(self.words)
        BagOfWords.lemmatize_words(self.words)
        self.freq_chart = BagOfWords.create_frequency_chart(self.words)

        # only plotting the frequency when a distinguishable name is provided
        if name is not None:
            BagOfWords.plot_frequency_chart(name, self.freq_chart)

    @staticmethod
    def tokenize(corpus: Union[str, list]) -> list:
        """Performs word tokenization of a corpus

        :param corpus: a single article or multiple articles
        :type textual_content: Union[str, list]
        :return: individual words occuring in the article(s)
        :rtype: list
        """

        # creating a list to store the words to be found
        words = []

        # separating cases for a single article vs multiple articles
        if isinstance(corpus, str):
            for word in word_tokenize(corpus):
                words.append(word)
        else:
            # looping through the articles and tokenizing each one individually
            for article in corpus:
                for word in word_tokenize(article):
                    words.append(word)
        return words

    @staticmethod
    def to_lower_case(words: list) -> None:
        """Converts each word to its lowercase derivative

        :param words: a vocabulary of words
        :type words: list[str]
        """

        for i in range(len(words)):
            words[i] = words[i].lower()

    @staticmethod
    def clean_data(words: list) -> None:
        """Performs text cleaning by removing links, times, dates, and prefix & suffix punctuation

        :param words: a vocabulary of words to be cleaned up
        :type words: list
        """

        noise = ['...', "n't"]

        def __is_time_or_date(word: str) -> bool:
            """Determines whether a string is either a time or date

            :param word: string containing word to be validated
            :type word: str
            :return: if the word is a time or date
            :rtype: bool
            """
            try:
                _ = parse(word)
                return True
            except Exception:
                return False

        def __is_link(word: str) -> bool:
            """Determines whether a string is a link

            :param word: string containing word to be validated
            :type word: str
            :return: if the word is a link
            :rtype: bool
            """
            # a list containing common domains
            suffixes = ['.com', '.org', '.edu', '.gov', '.int', '.co', '.net', '.au', '.us', '.uk', '.ne', 'news']

            # looping over domains to verify if any of them exist in the word
            for suffix in suffixes:
                if suffix in word:
                    return True
            return False

        # looping over words to see if any words (a) should be removed or (b) require trimming of a certain prefix and suffix
        for i in range(len(words)-1, -1, -1):
            if len(words[i]) <= 2 or words[i].isnumeric() or __is_time_or_date(words[i]) or words[i] in noise or __is_link(words[i]) or words[i] in [letter for letter in string.ascii_lowercase]:
                # TODO: change the last line to set(string.ascii_lowercase)
                words.pop(i)
                continue

            # shave punctation off of beginnings and from the end
            # TODO: change two checks into their own function to make code shorter
            start_ind, end_ind = -1, -1
            for j in range(len(words[i])):
                if words[i][j] in string.ascii_lowercase or words[i][j].isnumeric():
                    start_ind = j
                    break
            for j in range(len(words[i])-1, -1, -1):
                if words[i][j] in string.ascii_lowercase or words[i][j].isnumeric():
                    end_ind = j
                    break

            # checking for invalid situation
            if (start_ind == 0 and end_ind == len(words[i])-1) or start_ind >= end_ind:
                continue

            # trimming the current word down
            words[i] = words[i][start_ind:end_ind+1]

    @staticmethod
    def remove_stop_words(words: list) -> None:
        """Removes stop words

        :param words: a vocabulary of words containing stop words
        :type words: list[str]
        """

        # looping in reverse to delete elements
        for i in range(len(words)-1, -1, -1):
            if words[i] in set(stopwords.words('english')):
                words.pop(i)

    @staticmethod
    def lemmatize_words(words: list) -> None:
        """Performs lemmatization with nltk's WordNetLemmatizer()

        :param words: a vocabulary of words to individually be lemmatized
        :type words: list
        """

        def __get_part_of_speech(provided_word: str) -> str:
            """Determine the part of speech for a word

            :param provided_word: word whose part of speech is to be determined
            :type provided_word: str
            :return: a single character code denoting the part of speech (as per the lemmatizer's format)
            :rtype: str
            """

            # determining the part of speech for the provided word
            _, part_of_speech = nltk.pos_tag([provided_word])[0]

            # returning specific case-wise character codes based on the lemmatizer's specifications
            if 'NN' in part_of_speech:
                return 'n'
            if 'VB' in part_of_speech:
                return 'v'
            if 'JJ' in part_of_speech:
                return 'a'
            if 'RB' in part_of_speech:
                return 'r'
            return 'n'

        # initializing a lemmatizater
        lemmatizer = WordNetLemmatizer()

        # looping over the words and reassigning their lemmatized version
        for i in range(len(words)):
            words[i] = lemmatizer.lemmatize(words[i], __get_part_of_speech(words[i]))

        # perform some data cleaning on lemmatized words
        for i in range(len(words)-1, -1, -1):
            if words[i] in [letter for letter in string.ascii_lowercase]:
                # TODO: replace this with set(string.ascii_lowercase) to get faster results
                words.pop(i)

    @staticmethod
    def create_frequency_chart(words: list) -> dict:
        """Creates a frequency chart for a vocabulary of words

        :param words: a vocabulary of words
        :type words: list
        :return: a dictionary containing key-value pairs denoting word and frequency
        :rtype: dict
        """

        # creating a dictionary to store count for each word
        freq_chart = {}

        # looping over the words to add them to the dictionary
        for word in words:
            # case-wise evaluation of necessary increment
            if word not in freq_chart:
                freq_chart[word] = 1
            else:
                freq_chart[word] += 1

        # converting to list and sorting in ascending order by value
        sorted_freq_chart = sorted(freq_chart, key=freq_chart.get, reverse=True)

        # tranforming the sorted list back to a dictionary
        return {word: freq_chart[word] for word in sorted_freq_chart}

    @staticmethod
    def plot_frequency_chart(name: str, freq_chart: dict) -> None:
        """Plots frequency chart based on word frequency

        :param name: the header to be displayed for the plotting
        :type name: str
        :param freq_chart: a dictionary containing key-value pairs in the form: (word, frequency)
        :type freq_chart: dict
        """

        # picking apart the keys and values from the provided dictionary
        words = list(freq_chart.keys())[:100]
        frequencies = list(freq_chart.values())[:100]

        # modifying the settings for the plot
        plt.figure(figsize=(20, 5))
        plt.margins(x=0, tight=True)
        plt.bar(words, frequencies, color ='green')
        plt.tick_params(axis='x', which='major', labelsize=9)
        plt.xticks(rotation = 90)

        # setting title and labels
        plt.xlabel("Distinct Words")
        plt.ylabel(f"Frequency of Words in {name}")
        plt.title("Frequency Chart")

        # loading the plot
        plt.show()
