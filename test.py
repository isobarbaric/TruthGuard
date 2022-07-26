
import json
from newspaper import Article

# issues with (double slashes after name + repeating website name)
# first run:
# - 29/483 failed for conspiracy articles
# - 49/307 failed for science articles
# second run:
# - 20/481 failed for conspiracy articles
# - 19/314 failed for science articles

covid_articles = []
not_working = 0

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

with open('extract/conspiracy.json', 'r') as f:
    json_str = json.loads(f.read())
    for index, article_ref in enumerate(json_str):
        print(index+1, '/', len(json_str))
        modified_link = article_ref[1] 

        # remove double slash after first occurence
        if modified_link.find('http://') == -1 and modified_link.find('https://') == -1:
            modified_link = rreplace(modified_link, '//', '/', modified_link.count('//'))
            modified_link = 'https://' + modified_link
        else:
            modified_link = rreplace(modified_link, '//', '/', modified_link.count('//')-1)

        try:
            rn = Article(modified_link)
            rn.download()
            rn.parse()
            covid_articles.append([rn.title, rn.text])
        except Exception as e:
            not_working += 1
            print(modified_link)

with open('json_test/conspiracy.json', 'w') as f:
    f.write(json.dumps(covid_articles, indent = 4))

print(not_working)