
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import string
from matplotlib.ticker import MaxNLocator

class BagOfWords:

    def __init__(self, text, isPositive):
        # parameters and attributes
        self.text = text
        self.isPositive = isPositive

        # method calls
        self.tokenize()
        self.toLowerCase()
        self.removeStopWords()
        self.createFrequencyChart()
        self.generateVector()

    def tokenize(self):
        self.sentences = sent_tokenize(self.text)
        self.words = []
        for sentence in self.sentences:
            self.words.append([])
            for word in word_tokenize(sentence):
                self.words[-1].append(word)

    def toLowerCase(self):
        for sentence in self.words:
            for i in range(len(sentence)):
                sentence[i] = sentence[i].lower()

    def removeStopWords(self):
        for i in range(len(self.words)):
            for j in range(len(self.words[i])-1, -1, -1):
                if self.words[i][j] in stopwords.words('english'):
                    self.words[i].pop(j)  

    def createFrequencyChart(self):
        self.freqChart = dict()
        for sentence in self.words:
            for word in sentence:
                if word not in self.freqChart.keys():
                    self.freqChart[word] = 1
                else:
                    self.freqChart[word] += 1
        # remove punctuation
        for existing_key in self.freqChart.copy():
            if existing_key in string.punctuation:
                del self.freqChart[existing_key]

        # sorting in ascending order by value 
        self.freqChart = {i: self.freqChart[i] for i in sorted(self.freqChart, key=self.freqChart.get)}

    def generateVector(self):
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
        words = list(self.freqChart.keys())
        frequencies = list(self.freqChart.values())

        # setup so that pyplot only uses integers on the y-axis
        ax = plt.figure().gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        # setting title and labels 
        plt.xlabel("Distinct Words")
        plt.ylabel("Frequency of Words")
        plt.title("Frequency Chart")

        ## end of configuration
        plt.bar(words, frequencies, color = 'lightgreen')
        plt.xticks(rotation = 90)

        # loading the plot
        plt.show()

a = '''Python uses duck typing and has typed objects but untyped variable names. Type constraints are not checked at compile time; rather, operations on an object may fail, signifying that it is not of a suitable type. Despite being dynamically-typed, Python is strongly-typed, forbidding operations that are not well-defined (for example, adding a number to a string) rather than silently attempting to make sense of them.

Python allows programmers to define their own types using classes, most often used for object-oriented programming. New instances of classes are constructed by calling the class and the classes are instances of the metaclass type (itself an instance of itself), allowing metaprogramming and reflection.

Before version 3.0, Python had two kinds of classes (both using the same syntax): old-style and new-style, current Python versions only support the semantics new style.

The long-term plan is to support gradual typing. Python's syntax allows specifying static types, but they are not checked in the default implementation, CPython.'''

b = BagOfWords(a, False)

b.plotFrequencyChart()

for row in b.vector:
    print(row)



