import json
from article_finder import ArticleFinder
from bag_of_words import BagOfWords

scientific_titles = None
conspiracy_titles = None

def load(which):
    global scientific_titles, conspiracy_titles

    if which:
        scientific_titles = []
        with open('json/related-articles_pro-science.json', 'r') as storage:
            info = json.loads(storage.read())
            for article in info:
                scientific_titles.append(article[0])
       
        conspiracy_titles = [] 
        with open('json/related-articles_conspiracy.json', 'r') as storage:
            info = json.loads(storage.read())
            for article in info:
                conspiracy_titles.append(article[0])
    else:
        a = ArticleFinder('https://mediabiasfactcheck.com/pro-science/')
        b = ArticleFinder('https://mediabiasfactcheck.com/conspiracy/')

        scientific_titles = [x for [x, y] in a.articles]
        conspiracy_titles = [x for [x, y] in b.articles]

load(True)

a = BagOfWords(scientific_titles, True, True)
b = BagOfWords(conspiracy_titles, False, True)

common_words = dict()

for word, count in a.freqChart.items():
    if word in b.freqChart:
        diff_count = count - b.freqChart[word]
        common_words[word] = diff_count/(count + b.freqChart[word])

common_words = {i: common_words[i] for i in sorted(common_words, key=common_words.get, reverse=True)}

sorted_words = []
for key, value in common_words.items():
    sorted_words.append([key, abs(value)])

sorted_words.sort(key=lambda x: x[1], reverse=True)

relevant_words = sorted_words[:20]
print(relevant_words)

