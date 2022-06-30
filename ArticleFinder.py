
from bs4 import BeautifulSoup
import requests
import os
import shutil
import time
import json

class ArticleFinder:
    
    suffixes = ['.com', '.org', '.edu', '.gov', '.int', '.co', '.net', '.au', '.us', '.uk', '.ne', 'news'] 
    
    covid_keywords = ['COVID', 'COVID-19', 'covid', 'pandemic', 'Pandemic', 'virus', 'Omicron', 'omicron', 'Delta', 'delta', 'variant', 'outbreak', 'mask', 'N95', 'KN95', 'wave', 'symptoms', 'testing', 'rapid test', 'pcr', 'PCR', 'social distancing', 'Social distancing', 'Social Distancing', 'epidemic', 'Epidemic', 'fatality rate', 'Fatality rate', 'Fatality Rate', 'flattening the curve', 'Flattening the Curve']

    where_to_look = ['div', 'section', 'span']

    dysfunctional_pages = ['ieee.org', 'www.naturalawakeningsmag.com', 'libertyvideos.org']

    def __init__(self, url):
        self.url = url
        self.crawl()
        self.articles = self.find_articles()
        with open('related-articles' + self.url[self.url.find('.com') + len('.com'):].replace('/', '_')[:-1] + '.json', 'w') as storage:
            storage.write(json.dumps(self.articles, indent = 4).replace('[', '{').replace(']', '}'))

    def crawl(self):
        self.html_page = requests.get(self.url) 
        soup = BeautifulSoup(self.html_page.content, 'lxml') 
        news_sites = soup.find_all('span', {'style': 'font-size: 12pt;'}) 
        webpages = [] 
        for news_channel in news_sites: 
            link = news_channel.text[news_channel.text.rfind('(')+1:-1]
            if link[-4:] in ArticleFinder.suffixes:
                if (link[:8] == 'https://'):
                    webpages.append(link[8:])
                else:
                    webpages.append(link)
        
        if 'news_channels' in os.listdir():
            shutil.rmtree('news_channels/')

        os.mkdir('news_channels') 

        for website in webpages: 
            if website in ArticleFinder.dysfunctional_pages:
                continue

            print(website) 

            try:
                current_html = str(requests.get('https://' + website).content) 
                with open('news_channels/' + website + 'html_page.txt', 'w') as rn: 
                    rn.write(current_html)
            except Exception:
                pass

        print("Located all Webpages...") 

    def find_articles(self):
        base_path = "news_channels/" 

        structure = os.listdir('news_channels/') 

        overall = [] 

        for file in structure:
            current_path = base_path + file 
        
            with open(current_path, 'r') as current_soup: 
                soup = BeautifulSoup(current_soup.read(), 'lxml') 
           
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
                    mod_title = article_title[1].text.replace('\\n', '').replace('\t', '').replace('\\r', '').replace('\\', '').replace('t', '')
                    mod_title = ' '.join(mod_title.split())

                    if 'css' in mod_title:
                        continue

                    for covid_word in ArticleFinder.covid_keywords: 
                        if covid_word in mod_title:
                            covid_related = True

                    if covid_related: 

                        intended_link = article_title[1]['href']

                        if intended_link[0] == '/':
                            intended_link = file[:-13] + intended_link

                        overall.append([mod_title, intended_link]) 
                        covid_related = False

        resultant = [] 

        for elem in overall: 
            if elem not in resultant:
                resultant.append(elem)

        return resultant
