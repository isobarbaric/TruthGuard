
import json
from newspaper import Article

# issues with (double slashes after name + repeating website name)
# should print out failed webpage names later
# 29/483 failed for conspiracy articles
# 49/307 failed for science articles

covid_articles = []
not_working = 0

with open('json_1/science.json', 'r') as f:
    json_str = json.loads(f.read())
    for index, article_ref in enumerate(json_str):
        print(index+1, '/', len(json_str))
        modified_link = article_ref[1] 
        if modified_link.find('http://') == -1 and modified_link.find('https://') == -1:
            modified_link = 'https://' + modified_link
        try:
            rn = Article(modified_link)
            rn.download()
            rn.parse()
            covid_articles.append([rn.title, rn.text])
        except Exception as e:
            not_working += 1
            print(modified_link)

with open('json_2/science.json', 'w') as f:
    f.write(json.dumps(covid_articles, indent = 4))

print(not_working)