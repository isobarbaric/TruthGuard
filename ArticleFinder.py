import json
from bs4 import BeautifulSoup
import requests

class ArticleFinder:
    
    suffixes = ['.com', '.org', '.edu', '.gov', '.int', '.co', '.net', '.au', '.us', '.uk', '.ne', 'news'] 
    
    covid_keywords = ['COVID', 'COVID-19', 'covid', 'pandemic', 'Pandemic', 'virus', 'Omicron', 'omicron', 'Delta', 'delta', 'variant', 'outbreak', 'mask', 'N95', 'KN95', 'wave', 'symptoms', 'testing', 'rapid test', 'pcr', 'PCR', 'social distancing', 'Social distancing', 'Social Distancing', 'epidemic', 'Epidemic', 'fatality rate', 'Fatality rate', 'Fatality Rate', 'flattening the curve', 'Flattening the Curve']

    where_to_look = ['div', 'section', 'span']

    dysfunctional_pages = ['ieee.org', 'www.naturalawakeningsmag.com', 'libertyvideos.org', 'retractionwatch.com']

    def __init__(self, url):
        self.url = url
        self.crawl()
        self.articles = self.find_articles()
        data_title = self.url[self.url.find('.com') + len('.com'):].replace('/', '_')[:-1]
        with open('json/related-articles' + data_title + '.json', 'w') as storage:
            storage.write(json.dumps(self.articles, indent = 4))

    def crawl(self):
        self.html_page = requests.get(self.url) 
        soup = BeautifulSoup(self.html_page.content, 'lxml') 
        news_sites = soup.find_all('span', {'style': 'font-size: 12pt;'}) 
        self.webpages = [] 
        
        for news_channel in news_sites: 
            link = news_channel.text[news_channel.text.rfind('(')+1:-1]
            if link[-4:] in ArticleFinder.suffixes:
                if (link[:8] == 'https://'):
                    self.webpages.append(link[8:])
                else:
                    self.webpages.append(link)

        self.html_contents = dict() 
        
        for website in self.webpages: 
            if website in ArticleFinder.dysfunctional_pages:
                continue

            print(website) 

            try:
                current_html = str(requests.get('https://' + website).content) 
                self.html_contents[website] = current_html
            except Exception:
                pass


    def find_articles(self):
        overall = [] 

        for file in self.html_contents.keys():
            soup = BeautifulSoup(self.html_contents[file], 'lxml') 
            potential_articles = [] 
            
            for i in range(3): 
                p1 = soup.find_all(ArticleFinder.where_to_look[i])
                p2 = []
          
                for potential in p1:
                    if potential.has_attr('class'):
                        p2.append(potential)

                for tag in p2:
                    for anchor in tag.find_all('a'):
                        if not anchor.has_attr('href'):
                            continue
                        potential_articles.append([tag, anchor])

            covid_related = False 
            for article_title in potential_articles: 
                intended_title = article_title[1].text.replace('\\n', '').replace('\t', '').replace('\\r', '').replace('\\', '')
                intended_title = ' '.join(intended_title.split())

                if 'css' in intended_title:
                    continue

                if 'http' in intended_title:
                    continue

                for covid_word in ArticleFinder.covid_keywords: 
                    if covid_word in intended_title:
                        covid_related = True

                if covid_related: 
                    intended_link = article_title[1]['href']
                    if intended_link[0] == '/':
                        intended_link = file + intended_link

                    overall.append([intended_title, intended_link]) 
                    covid_related = False

        resultant = [] 

        for article in overall:
            if article not in resultant:
                resultant.append(article)

        return resultant
