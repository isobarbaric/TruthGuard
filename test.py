
import json
from newspaper import Article

covid_articles = []

not_working = 0


with open('json_1/conspiracy.json', 'r') as f:
    json_str = json.loads(f.read())
    for index, article_ref in enumerate(json_str):
        print(index+1, '/', len(json_str))
        modified_link = article_ref[1] 
        if modified_link.find('http://') == -1 and modified_link.find('https://') == -1:
            modified_link = 'https://' + modified_link
        # print(modified_link)
        try:
            rn = Article(modified_link)
            rn.download()
            rn.parse()
            covid_articles.append([rn.title, rn.text])
        except Exception as e:
            # template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            # message = template.format(type(e).__name__, e.args)
            not_working += 1
            print(modified_link)

with open('json_2/conspiracy.json', 'w') as f:
    # f.write(str(covid_articles))
    f.write(json.dumps(covid_articles, indent = 4))

print(not_working)