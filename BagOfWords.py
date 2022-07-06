
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import nltk
import string
import re

class BagOfWords:

    lemmatizer = WordNetLemmatizer()
    punctuation = [a for a in string.punctuation] + [u'\u201c',u'\u201d',u'\u2018',u'\u2019']
    stopWords = set(stopwords.words('english'))

    def __init__(self, text, isPositive, separatedAlready):
        # parameters and attributes
        self.text = text
        self.isPositive = isPositive
        self.separatedAlready = separatedAlready

        # method calls
        self.tokenize()
        self.removeStopWords()
        self.toLowerCase()
        self.normalizeWords()
        self.createFrequencyChart()
        self.generateTable()

    @staticmethod
    def trimmer(word):
        # perform check
        if word.isnumeric():
            return '' 

        # remove all non-printable characters
        word = re.sub(r'[^\x00-\x7f]',r'', word)

        if len(word) == 0:
            return ''

        # condense string
        cnt = [ [word[0], 1] ]
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
        # return modified copy
        return revised_copy

    def tokenize(self):
        if not self.separatedAlready:
            self.sentences = sent_tokenize(self.text)
        else:
            self.sentences = self.text
        self.words = []
        for sentence in self.sentences:
            self.words.append([])
            for word in word_tokenize(sentence):
                revised_word = BagOfWords.trimmer(word)
                if len(revised_word) == 0:
                    continue
                self.words[-1].append(revised_word)

        # remove punctuation and symbols
        common_occuring_noise = ['...', "'s", '…']

        # iterates over sentences
        for i in range(len(self.words)):
            # iterates over words
            for j in range(len(self.words[i])-1, -1, -1):
                if self.words[i][j] in BagOfWords.punctuation or self.words[i][j] in common_occuring_noise:
                    self.words[i].pop(j) 
                    continue
                revised_word = self.words[i][j]
                # removing punctuation from inside a word
                for character in BagOfWords.punctuation:
                    revised_word = revised_word.replace(character, '')
                self.words[i][j] = revised_word

    def removeStopWords(self):
        for i in range(len(self.words)):
            for j in range(len(self.words[i])-1, -1, -1):
                if self.words[i][j] in BagOfWords.stopWords:
                    self.words[i].pop(j)  

    def toLowerCase(self):
        for sentence in self.words:
            for i in range(len(sentence)):
                sentence[i] = sentence[i].lower()

    # some inaccuracies, 'typed' returns noun
    @staticmethod
    def getPartOfSpeech(provided_word): 
        _, part_of_speech = nltk.pos_tag([provided_word])[0]

        if 'NN' in part_of_speech:
            return 'n'
        elif 'VB' in part_of_speech:
            return 'v'
        elif 'JJ' in part_of_speech:
            return 'a'
        elif 'RB' in part_of_speech:
            return 'r'

        return 'n'

    def normalizeWords(self):
        for i in range(len(self.words)):
            for j in range(len(self.words[i])):
                self.words[i][j] = BagOfWords.lemmatizer.lemmatize(self.words[i][j], BagOfWords.getPartOfSpeech(self.words[i][j]))

    def createFrequencyChart(self):
        self.freqChart = dict()
        for sentence in self.words:
            for word in sentence:
                if word not in self.freqChart.keys():
                    self.freqChart[word] = 1
                else:
                    self.freqChart[word] += 1

        # sorting in ascending order by value 
        self.freqChart = {i: self.freqChart[i] for i in sorted(self.freqChart, key=self.freqChart.get, reverse=True)}

    def generateTable(self):
        self.vector = []

        # adding the header         
        self.vector.append([])
        dict_keys = list(self.freqChart.keys())
        self.vector[-1].append(None)
        for i in range(len(dict_keys)):
            self.vector[-1].append(dict_keys[i])
        self.vector[-1].append(self.isPositive)

        # adding more rows to the vector
        for i in range(len(self.sentences)):
            to_add = [self.sentences[i]]
            for word in dict_keys:
                if word in self.words[i]:
                    to_add.append(1)
                else:
                    to_add.append(0)
            to_add.append(self.isPositive)
            self.vector.append(to_add)

    def plotFrequencyChart(self):

        # # frequency chart:
        plt.bar(self.freqChart.keys(), self.freqChart.values(), 10)
        plt.show()

        # # bar graph:

        # words = list(self.freqChart.keys())
        # frequencies = list(self.freqChart.values())

        # # setup so that pyplot only uses integers on the y-axis
        # ax = plt.figure().gca()
        # ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        # # setting title and labels 
        # plt.xlabel("Distinct Words")
        # plt.ylabel("Frequency of Words")
        # plt.title("Frequency Chart")

        # max_word_len = -1
        # for word in words:
        #     max_word_len = max(max_word_len, len(word))

        # # increasing space from bottom
        # plt.subplots_adjust(bottom=max_word_len/60)

        # # increase label size
        # plt.tick_params(axis='x', which='major', labelsize=2)

        # # increase the x-axis's length to prevent the labels from being squished together
        # graph_size = 40/plt.gcf().dpi*len(self.freqChart.keys())
        # plt.gcf().set_size_inches(graph_size, plt.gcf().get_size_inches()[1])

        # plt.bar(words, frequencies, color = 'lightgreen')
        # plt.xticks(rotation = 90)

        # # loading the plot
        # plt.show()

