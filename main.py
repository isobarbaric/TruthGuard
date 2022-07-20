import json
from article_finder import ArticleFinder
from bag_of_words import BagOfWords
from matplotlib import pyplot as plt

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

        scientific_titles = [x for [x, _] in a.articles]
        conspiracy_titles = [x for [x, _] in b.articles]

# load articles
load(True)

# instantiate two instances of BagOfWords
a = BagOfWords(scientific_titles, True, True)
b = BagOfWords(conspiracy_titles, False, True)

# determine common words between the two sets of words
common_words = dict()
for word, count in a.freqChart.items():
    if word in b.freqChart:
        diff_count = count - b.freqChart[word]
        common_words[word] = diff_count/(count + b.freqChart[word])

# remove all with count 0 and sorting it
common_words = dict(filter(lambda elem: elem[1] != 0, common_words.items()))
common_words = {i: common_words[i] for i in sorted(common_words, key=common_words.get, reverse=True)}

# plot a graph containing words on either side
x_axis, y_axis = [], []
for word, value in common_words.items():
    x_axis.append(word)
    y_axis.append(value)

plt.figure()
plt.xlabel("Distinct Words")
plt.ylabel("Adjusted Frequency")
plt.title("Most-Frequent Words")
plt.bar(x_axis, y_axis)
plt.subplots_adjust(bottom=0.3)
plt.gcf().set_size_inches(20, plt.gcf().get_size_inches()[1])
plt.tick_params(axis='x', which='major', labelsize=5)
plt.xticks(rotation = 90)
plt.show()

# extract 20 most common words
sorted_words = []
for key, value in common_words.items():
    sorted_words.append([key, abs(value)])
sorted_words.sort(key=lambda x: x[1], reverse=True)
relevant_words = sorted_words[:20]
print(relevant_words)



