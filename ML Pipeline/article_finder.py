
import os
import shutil
import requests
from bs4 import BeautifulSoup

class ArticleFinder:

    suffixes = ['.com', '.org', '.edu', '.gov', '.int', '.co', '.net', '.au', '.us', '.uk', '.ne', 'news']

    covid_keywords = ['COVID', 'COVID-19', 'covid', 'pandemic', 'Pandemic', 'virus', 'Omicron', 'omicron', 'Delta', 'delta', 'variant', 'outbreak', 'mask', 'N95', 'KN95', 'wave', 'symptoms', 'testing', 'rapid test', 'pcr', 'PCR', 'social distancing', 'Social distancing', 'Social Distancing', 'epidemic', 'Epidemic', 'fatality rate', 'Fatality rate', 'Fatality Rate', 'flattening the curve', 'Flattening the Curve']

    where_to_look = ['div', 'section', 'span']

    dysfunctional_pages = ['ieee.org', 'www.naturalawakeningsmag.com', 'libertyvideos.org']

    def __init__(self) -> None:
        pass

    def __crawler(self, url: str) -> None:
        """Crawls through MBFC provided links and stores their  content

        :param url: an MBFC link to a list of pages under a specific genre
        :type url: str
        """

        # access the MBFC page linked via the url parameter
        html_page = requests.get(url)

        # parse through that particular page and find all of the news sites
        soup = BeautifulSoup(html_page.content, 'lxml')
        news_sites = soup.find_all('span', {'style': 'font-size: 12pt;'})

        # creating storage for all of the links to be obtained off the MBFC page
        webpages = []

        # loop through the links found
        for news_channel in news_sites:
            # parse through list item and extract just the link
            link = news_channel.text[news_channel.text.rfind('(')+1:-1]

            # adjust the link based on if the 'https' prefix is present
            if link[-4:] in ArticleFinder.suffixes:

                # add the modified link for storage
                if (link[:8] == 'https://'):
                    webpages.append(link[8:])
                else:
                    webpages.append(link)

        # delete scraped content if it exists currently
        if 'news_channels' in os.listdir():
            shutil.rmtree('news_channels/')

        # create a new directory to store the scraped content
        os.mkdir('news_channels')

        # loop through the webpages and access their
        for website in webpages:

            # if the website is a dysfunctional one, then skip over the current iteration
            if website in ArticleFinder.dysfunctional_pages:
                continue

            try:
                # access the current website's HTML and save it to a variable
                current_html = str(requests.get('https://' + website).content)

                # creating a new file in the current directory and saving the HTML accessed earlier to this file
                with open('news_channels/' + website + 'html_page.txt', 'w') as rn:
                    rn.write(current_html)

            except Exception:
                # if the html cannot be obtained, then continue and skip over the current iteration
                pass

    def __finder(self) -> list:
        """Finds articles when given

        :return: a list of article objects (dict)
        :rtype: list
        """
        # create a variable to store the base path to avoid subsequent duplication 
        base_path = "news_channels/"

        # locate all of the files under the base directory, i.e. the parsed news sites found from the url provided to MBFC
        structure = os.listdir(base_path)

        # creating a variable to store the articles found
        overall = []

        # loop through the files located under the base directory
        for file in structure:
            # using a combination of a relative and absolute path, determine the exact path to the current file
            current_path = base_path + file

            # open the current file to read its contents
            with open(current_path, 'r') as current_soup:

                # parsing the current file's HTML contents
                soup = BeautifulSoup(current_soup.read(), 'lxml')

                # creating a variable to store potential articles, to be added to the overall list after validation
                potential_articles = []

                # looping over all possible locations where the articles can occur
                for i in range(3):
                    # applying a two-step check to find news articles
                    p1 = soup.find_all(ArticleFinder.where_to_look[i])
                    p2 = []

                    # looping over the occurences of the HTML element
                    for potential in p1:
                        # applying a condition to determine eligibility
                        if potential.has_attr('class'):
                            p2.append(potential)

                    # looping over tags of screened HTML elements from the artiles
                    for tag in p2:
                        # looping over those elements with an anchor attribute
                        for anchor in tag.find_all('a'):
                            # applying a condition to determine eligibility
                            if not anchor.has_attr('href'):
                                continue
                            potential_articles.append(anchor)

                # using a set() to remove duplicate article entries
                potential_articles = list(set(potential_articles))

                # validating whether approved articles are related to COVID-19 or not
                covid_related = False
                for article_title in potential_articles:

                    # cleaning up article text
                    mod_title = article_title.text
                    mod_title = ' '.join(mod_title.split())

                    # further screening checks to vet out any CSS
                    if 'css' in mod_title:
                        continue

                    # checking if the current article is related to COVID-19 or not based on COVID-19 keywords defined above
                    for covid_word in ArticleFinder.covid_keywords:
                        if covid_word in mod_title:
                            covid_related = True

                    # adding the current article to the list of articles if it is COVID-19 related
                    if covid_related:

                        # accessing the current title
                        intended_link = article_title['href']

                        # applying case-wise modifications to tidy up the url
                        if intended_link[0] == '/' or intended_link[0] not in ['h', 'w']:
                            intended_link = file[:-13] + intended_link
                        if intended_link.count('http://') + intended_link.count('https://') == 0:
                            intended_link = 'https://' + intended_link

                        # creating a dictionary object to store the current article's parts
                        article = {
                            'title': mod_title,
                            'link': intended_link,
                        }

                        # adding the current article to storage
                        overall.append(article)

                        # resetting parameters to be checked
                        covid_related = False

        return overall

    def find_articles(self, url: str) -> list:
        """Finds articles based on the MBFC link provided

        :param url: an MBFC link to a list of pages under a specific genre
        :type url: str
        :return: a list of article objects (dict)
        :rtype: list
        """

        # calling crawler and finder to obtain
        self.__crawler(url)
        articles = self.__finder()

        # deleting the directory containing the articles as they are no longer needed
        shutil.rmtree('news_channels/')

        return articles