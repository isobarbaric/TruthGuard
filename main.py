from ArticleFinder import ArticleFinder
from BagOfWords import BagOfWords
import json

a = ArticleFinder('https://mediabiasfactcheck.com/pro-science/')
b = ArticleFinder('https://mediabiasfactcheck.com/conspiracy/')

def load_conspiracy():
    titles = []
    with open('json/related-articles_conspiracy.json', 'r') as storage:
        info = json.loads(storage.read())
        for article in info:
            titles.append(article[0])
    return titles

def load_science():
    titles = []
    with open('json/related-articles_pro-science.json', 'r') as storage:
        info = json.loads(storage.read())
        for article in info:
            titles.append(article[0])
    return titles

scientific_titles = load_science()
conspiracy_titles = load_conspiracy()

a = BagOfWords(scientific_titles, True, True)
b = BagOfWords(conspiracy_titles, False, True)
print(a.freqChart, '\n\n\n', b.freqChart)

# a.plotFrequencyChart()
# b.plotFrequencyChart()


