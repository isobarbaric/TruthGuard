
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import nltk
import re
import string

class BagOfWords:

    lemmatizer = WordNetLemmatizer()
    punctuation = list(string.punctuation) + [u'\u201c',u'\u201d',u'\u2018',u'\u2019']
    stopWords = set(stopwords.words('english') + list(string.ascii_lowercase) + list(string.ascii_uppercase))
    unwanted = ['x01', 'x02', 'x03', 'x04', 'x05', 'x06', 'x07', 'x08', 'x09', 'x0a', 'x0b', 'x0c', 'x0d', 'x0e', 'x0f', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x1a', 'x1b', 'x1c', 'x1d', 'x1e', 'x1f', 'x20', 'x21', 'x22', 'x23', 'x24', 'x25', 'x26', 'x27', 'x28', 'x29', 'x2a', 'x2b', 'x2c', 'x2d', 'x2e', 'x2f', 'x30', 'x31', 'x32', 'x33', 'x34', 'x35', 'x36', 'x37', 'x38', 'x39', 'x3a', 'x3b', 'x3c', 'x3d', 'x3e', 'x3f', 'x40', 'x41', 'x42', 'x43', 'x44', 'x45', 'x46', 'x47', 'x48', 'x49', 'x4a', 'x4b', 'x4c', 'x4d', 'x4e', 'x4f', 'x50', 'x51', 'x52', 'x53', 'x54', 'x55', 'x56', 'x57', 'x58', 'x59', 'x5a', 'x5b', 'x5c', 'x5d', 'x5e', 'x5f', 'x60', 'x61', 'x62', 'x63', 'x64', 'x65', 'x66', 'x67', 'x68', 'x69', 'x6a', 'x6b', 'x6c', 'x6d', 'x6e', 'x6f', 'x70', 'x71', 'x72', 'x73', 'x74', 'x75', 'x76', 'x77', 'x78', 'x79', 'x7a', 'x7b', 'x7c', 'x7d', 'x7e', 'x7f', 'x80', 'x81', 'x82', 'x83', 'x84', 'x85', 'x86', 'x87', 'x88', 'x89', 'x8a', 'x8b', 'x8c', 'x8d', 'x8e', 'x8f', 'x90', 'x91', 'x92', 'x93', 'x94', 'x95', 'x96', 'x97', 'x98', 'x99', 'x9a', 'x9b', 'x9c', 'x9d', 'x9e', 'x9f', 'xa0', 'xa1', 'xa2', 'xa3', 'xa4', 'xa5', 'xa6', 'xa7', 'xa8', 'xa9', 'xaa', 'xab', 'xac', 'xad', 'xae', 'xaf', 'xb0', 'xb1', 'xb2', 'xb3', 'xb4', 'xb5', 'xb6', 'xb7', 'xb8', 'xb9', 'xba', 'xbb', 'xbc', 'xbd', 'xbe', 'xbf', 'xc0', 'xc1', 'xc2', 'xc3', 'xc4', 'xc5', 'xc6', 'xc7', 'xc8', 'xc9', 'xca', 'xcb', 'xcc', 'xcd', 'xce', 'xcf', 'xd0', 'xd1', 'xd2', 'xd3', 'xd4', 'xd5', 'xd6', 'xd7', 'xd8', 'xd9', 'xda', 'xdb', 'xdc', 'xdd', 'xde', 'xdf', 'xe0', 'xe1', 'xe2', 'xe3', 'xe4', 'xe5', 'xe6', 'xe7', 'xe8', 'xe9', 'xea', 'xeb', 'xec', 'xed', 'xee', 'xef', 'xf0', 'xf1', 'xf2', 'xf3', 'xf4', 'xf5', 'xf6', 'xf7', 'xf8', 'xf9', 'xfa', 'xfb', 'xfc', 'xfd', 'xfe', 'xff'] + ['—']

    def __init__(self, text, is_positive, separated_already):
        # parameters and attributes
        self.text = text
        self.is_positive = is_positive
        self.separated_already = separated_already

        # method calls
        self.tokenize()
        self.to_lower_case()
        self.remove_stop_words()
        self.normalize_words()
        self.create_frequency_chart()
        self.generate_table()

    @staticmethod
    def trimmer(word):
        if word.isnumeric():
            return ''

        if len(word) == 0:
            return ''

        # condense string
        cnt = [[word[0], 1]]
        ptr = 0
        for i in range(1, len(word)):
            if word[i] == word[i-1]:
                cnt[ptr][1] += 1
            else:
                cnt.append([word[i], 1])
                ptr += 1
        revised_copy = ''
        for condensed in cnt:
            if condensed[0] == 't' and condensed[1] > 2:
                continue
            revised_copy += (condensed[0] * condensed[1])

        for elem in BagOfWords.unwanted:
            if elem in revised_copy:
                revised_copy = revised_copy.replace(elem, '')
        # return modified copy
        return revised_copy

    def tokenize(self):
        if not self.separated_already:
            self.sentences = sent_tokenize(self.text)
        else:
            self.sentences = self.text
        self.words = []
        for sentence in self.sentences:
            self.words.append([])
            for word in word_tokenize(sentence):
                self.words[-1].append(word)

        # remove punctuation and symbols
        common_occuring = ['...', "'s", '…']

        # iterates over sentences
        for i in range(len(self.words)):
            # iterates over words
            for j in range(len(self.words[i])-1, -1, -1):
                if self.words[i][j] in BagOfWords.punctuation or self.words[i][j] in common_occuring:
                    self.words[i].pop(j)
                    continue
                revised_word = self.words[i][j]
                # removing punctuation from inside a word
                for character in BagOfWords.punctuation:
                    revised_word = str(revised_word).replace(character, '')
                self.words[i][j] = revised_word

        # iterates over sentences
        for i in range(len(self.words)):
            # iterates over words
            for j in range(len(self.words[i])-1, -1, -1):
                revised_word = BagOfWords.trimmer(self.words[i][j])
                if len(revised_word) == 0:
                    continue
                self.words[i][j] = revised_word

    def remove_stop_words(self):
        for i in range(len(self.words)):
            for j in range(len(self.words[i])-1, -1, -1):
                if self.words[i][j] in BagOfWords.stopWords or len(self.words[i][j]) == 0:
                    self.words[i].pop(j)  

    def to_lower_case(self):
        for sentence in self.words:
            for i in range(len(sentence)):
                sentence[i] = sentence[i].lower()

    # some inaccuracies, 'typed' returns noun
    @staticmethod
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

    def normalize_words(self):
        for i in range(len(self.words)):
            for j in range(len(self.words[i])):
                self.words[i][j] = BagOfWords.lemmatizer.lemmatize(self.words[i][j], BagOfWords.get_part_of_speech(self.words[i][j]))

    def create_frequency_chart(self):
        self.freqChart = dict()
        for sentence in self.words:
            for word in sentence:
                if word not in self.freqChart.keys():
                    self.freqChart[word] = 1
                else:
                    self.freqChart[word] += 1

        # sorting in ascending order by value
        self.freqChart = {i: self.freqChart[i] for i in sorted(self.freqChart, key=self.freqChart.get, reverse=True)}

    def generate_table(self):
        self.vector = []

        # adding the header         
        self.vector.append([])
        dict_keys = list(self.freqChart.keys())
        self.vector[-1].append(None)
        for i in range(len(dict_keys)):
            self.vector[-1].append(dict_keys[i])
        self.vector[-1].append(self.is_positive)

        # adding more rows to the vector
        for i in range(len(self.sentences)):
            to_add = [self.sentences[i]]
            for word in dict_keys:
                if word in self.words[i]:
                    to_add.append(1)
                else:
                    to_add.append(0)
            to_add.append(self.is_positive)
            self.vector.append(to_add)

    def plot_frequency_chart(self):

        # # frequency chart:
        # plt.bar(self.freqChart.keys(), self.freqChart.values(), 10)
        # plt.show()

        # # bar graph:

        words = list(self.freqChart.keys())[:200]
        frequencies = list(self.freqChart.values())[:200]

        # setup so that pyplot only uses integers on the y-axis
        ax = plt.figure().gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        # setting title and labels
        plt.xlabel("Distinct Words")
        plt.ylabel(f"Frequency of Words in {self.is_positive}")
        plt.title("Frequency Chart")

        max_word_len = -1
        for word in words:
            max_word_len = max(max_word_len, len(word))

        # increasing space from bottom
        plt.subplots_adjust(bottom=max_word_len/60)

        # increase label size
        plt.tick_params(axis='x', which='major', labelsize=6)

        # increase the x-axis's length to prevent the labels from being squished together
        graph_size = 40/plt.gcf().dpi*len(self.freqChart.keys())
        plt.gcf().set_size_inches(graph_size, plt.gcf().get_size_inches()[1])

        plt.bar(words, frequencies, color = 'lightgreen')
        plt.xticks(rotation = 90)

        # loading the plot
        plt.show()

