
from nltk import word_tokenize

# extracting an article from a link
link = 'https://www.genengnews.com/news/omicron-subvariants-ba-4-and-ba-5-are-more-elusive-to-immune-system/'

element = ['div', 'article', 'section', 'span', 'p']
attr = ['article', 'content', 'post', 'text', 'news']

import requests
from bs4 import BeautifulSoup

html = requests.get(link)
soup = BeautifulSoup(html.text, 'html.parser')

articles = []

for html_tag in element:
    for potential in soup.find_all(html_tag):
        if potential.has_attr('class'):
            exists = False
            if len(potential['class']) == 0:
                continue
            for pos_attr in attr:
                if potential['class'][0].count(pos_attr) > 0:
                    exists = True
            if exists:
                print(potential['class'][0])
                exists = False
            articles.append(potential.text.strip())

for i in range(len(articles)-1, -1, -1):
    if len(word_tokenize(articles[i])) <= 20:
        # print(lenarticles[i])
        articles.pop(i)

print(articles)

with open('test.txt', 'w') as f:
    for article in articles:
        print(len(word_tokenize(article)))
        f.write(article + '\n\n')