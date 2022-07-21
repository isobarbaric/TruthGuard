
import newspaper
from newspaper import Config, ArticleException
import requests
import json
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
                webpages.append(link)
            else:
                webpages.append('https://' + link)
    return webpages



def retrieve_store_articles(url, name):
    # word-validation is not the best -> maybe get rid of overlapping words
    covid_keywords = ['COVID', 'COVID-19', 'covid', 'pandemic', 'Pandemic', 'virus', 'Omicron', 'omicron', 'Delta', 'delta', 'variant', 'outbreak', 'mask', 'N95', 'KN95', 'wave', 'symptoms', 'testing', 'rapid test', 'pcr', 'PCR', 'social distancing', 'Social distancing', 'Social Distancing', 'epidemic', 'Epidemic', 'fatality rate', 'Fatality rate', 'Fatality Rate', 'flattening the curve', 'Flattening the Curve']
    covid_keywords = [word.lower() for word in covid_keywords]
    covid_keywords = list(set(covid_keywords))

    articles = []

    for link in get_urls(url)[:5]:
        current_articles = newspaper.build(link, memoize_articles = False)
        articles.append(current_articles)
        print(link, len(current_articles.articles))

    data = []

    for website in articles:    
        # have to limit the number of articles because of computational constraints
        cnt = 0
        for article in website.articles:
            if cnt == 5:
                break
            try:
                article.download()
                article.parse()
                keyword_occ = 0
                for word in covid_keywords:
                    if word in article.text.lower():
                        keyword_occ += 1
                print(keyword_occ)
                if keyword_occ <= 1:
                    continue
                data.append([article.url, article.text])
                cnt += 1
            except ArticleException:
                pass

    with open('json/related-articles_' + name + '.json', 'w') as f:
        f.write(json.dumps(data, indent = 4))

# try using these later on 
config = Config()
config.memoize_articles = False

retrieve_store_articles('https://mediabiasfactcheck.com/pro-science/', 'pro-science')
retrieve_store_articles('https://mediabiasfactcheck.com/conspiracy/', 'conspiracy')
