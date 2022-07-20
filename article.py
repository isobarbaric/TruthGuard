import newspaper

import requests
from bs4 import BeautifulSoup

def get_urls(url):
   html_page = requests.get(url)
   soup = BeautifulSoup(html_page.text, 'lxml')
   news_sites = soup.find_all('span', {'style': 'font-size: 12pt;'})
   suffixes = ['.com', '.org', '.edu', '.gov', '.int', '.co', '.net', '.au', '.us', '.uk', '.ne', 'news']
   webpages = []
   for news_channel in news_sites:
      link = news_channel.text[news_channel.text.rfind('(')+1:-1]
      if link[-4:] in suffixes:
            if link[:8] == 'https://':
               webpages.append(link[8:])
            else:
               webpages.append(link)

   return webpages

print(get_urls('https://mediabiasfactcheck.com/pro-science/'))
print(get_urls('https://mediabiasfactcheck.com/conspiracy/'))

cnn_paper = newspaper.build('http://cnn.com')
print(type(cnn_paper))

# for article in cnn_paper.articles:
#    print(article.url)

# for category in cnn_paper.category_urls():
#      print(category)

# http://lifestyle.cnn.com
# http://cnn.com/world
# http://tech.cnn.com

# cnn_article = cnn_paper.articles[0]
# cnn_article.download()
# cnn_article.parse()
# cnn_article.nlp()