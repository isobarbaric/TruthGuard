import json
import requests
from bs4 import BeautifulSoup

# add type stuff to functions
class ArticleFinder:
    COVID_KEYWORDS = ['COVID', 'COVID-19', 'covid', 'pandemic', 'Pandemic', 'virus', 'Omicron', 'omicron', 'Delta', 'delta', 'variant', 'outbreak', 'mask', 'N95', 'KN95', 'wave', 'symptoms', 'testing', 'rapid test', 'pcr', 'PCR', 'social distancing', 'Social distancing', 'Social Distancing', 'epidemic', 'Epidemic', 'fatality rate', 'Fatality rate', 'Fatality Rate', 'flattening the curve', 'Flattening the Curve']
    HTML_TAGS = ['div', 'section', 'span']

    def __init__(self) -> None:
        pass

    @staticmethod
    def __crawler(article_type) -> None:
        """Crawls through MBFC provided links and stores their content

        :param url: an MBFC link to a list of pages under a specific genre
        :type url: str
        """

        # read webpages from data directory
        if article_type == "science":
            with open('data/website_metadata/science.json') as file:
                sites = json.load(file)
        else:
            with open('data/website_metadata/conspiracy.json') as file:
                sites = json.load(file)

        pages = []

        # loop through the webpages
        for site in sites:
            try:
                # access the current website's HTML and save it to a variable
                current_html = str(requests.get(site['url'], timeout=1).content)
                pages.append({"url": site['url'], "html": current_html})
            except Exception:
                # print(f"... error raised with {site['name']}")
                pass
        
        return pages

    @staticmethod
    def __finder(pages) -> list:
        """Finds articles when given

        :return: a list of article objects
        :rtype: list
        """
        # creating a variable to store the articles found
        overall = []

        # loop through the files located under the base directory
        for page in pages:
            # parsing the current file's HTML contents
            soup = BeautifulSoup(page['html'], 'lxml')

            # creating a variable to store potential articles, to be added to the overall list after validation
            potential_articles = []

            # looping over all possible locations where the articles can occur
            for i in range(3):
                # applying a two-step check to find news articles
                p1 = soup.find_all(ArticleFinder.HTML_TAGS[i])
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
                for covid_word in ArticleFinder.COVID_KEYWORDS:
                    if covid_word in mod_title:
                        covid_related = True

                # adding the current article to the list of articles if it is COVID-19 related
                if covid_related:
                    # accessing the current title
                    intended_link = article_title['href']

                    # applying case-wise modifications to tidy up the url
                    if intended_link[0] == '/' or intended_link[0] not in ['h', 'w']:
                        intended_link = page['url'] + intended_link
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

    @staticmethod
    def find_articles(article_type: str) -> list:
        """Finds articles based on the article type

        :param article_type: either "science" or "conspiracy"
        :type article_type: str
        :return: a list of article objects (dict)
        :rtype: list
        """

        if not (article_type == "science" or article_type == "conspiracy"):
            raise ValueError("article_type param must either be 'science' or 'conspiracy'")

        # calling crawler and finder to obtain all articles
        pages = ArticleFinder.__crawler(article_type)
        articles = ArticleFinder.__finder(pages)

        return articles
