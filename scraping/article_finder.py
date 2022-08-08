from bs4 import BeautifulSoup
import requests
import os
import shutil
from newspaper import Article

class ArticleFinder:
    
    suffixes = ['.com', '.org', '.edu', '.gov', '.int', '.co', '.net', '.au', '.us', '.uk', '.ne', 'news'] 
    
    covid_keywords = ['COVID', 'COVID-19', 'covid', 'pandemic', 'Pandemic', 'virus', 'Omicron', 'omicron', 'Delta', 'delta', 'variant', 'outbreak', 'mask', 'N95', 'KN95', 'wave', 'symptoms', 'testing', 'rapid test', 'pcr', 'PCR', 'social distancing', 'Social distancing', 'Social Distancing', 'epidemic', 'Epidemic', 'fatality rate', 'Fatality rate', 'Fatality Rate', 'flattening the curve', 'Flattening the Curve']

    where_to_look = ['div', 'section', 'span']

    dysfunctional_pages = ['ieee.org', 'www.naturalawakeningsmag.com', 'libertyvideos.org']

    def __init__(self):
        pass

    def find_articles(self, url):
        self.__crawler(url)
        articles = self.__finder()
        return articles

    def __crawler(self, url):
        html_page = requests.get(url) 
        soup = BeautifulSoup(html_page.content, 'lxml') 
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
            try:
                current_html = str(requests.get('https://' + website).content) 
                with open('news_channels/' + website + 'html_page.txt', 'w') as rn: 
                    rn.write(current_html)
            except Exception:
                pass

    def __finder(self):
        base_path = "news_channels/" 
        structure = os.listdir('news_channels/') 

        overall = [] 
        not_working = 0
        total_attempts = 0

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
                            potential_articles.append(anchor)
                potential_articles = list(set(potential_articles))

                covid_related = False 
                for article_title in potential_articles: 
                    mod_title = article_title.text
                    mod_title = ' '.join(mod_title.split())

                    if 'css' in mod_title:
                        continue

                    for covid_word in ArticleFinder.covid_keywords: 
                        if covid_word in mod_title:
                            covid_related = True

                    if covid_related: 

                        intended_link = article_title['href']

                        # if intended_link[0] not in ['h', 'w'] and intended_link != '/':
                        #     intended_link = '/' + intended_link

                        if intended_link[0] == '/' or intended_link[0] not in ['h', 'w']:
                            intended_link = file[:-13] + intended_link

                        if intended_link.count('http://') + intended_link.count('https://') == 0:
                            intended_link = 'https://' + intended_link

                        try:
                            total_attempts += 1
                            # rn = Article(intended_link)
                            # rn.download()
                            # rn.parse()
                            article = {
                                'title': mod_title,
                                'link': intended_link,
                                'text': "testing"
                            }
                            overall.append(article) 
                        except Exception as e:
                            print(intended_link)
                            not_working += 1

                        covid_related = False

        print("total dysfunctional: ", not_working, "; total attempts: ", total_attempts, sep='')

        return overall