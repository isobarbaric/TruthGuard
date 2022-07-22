
import json
import os

unwanted = ['back_matter', 'bib_entries', 'ref_entries']

# ensuring all data was in json format to begin with
# to be done rn 

# parsing and simplifying JSON data
for file in os.listdir('data'):
    path = 'data/' + file
    content = None
    with open(path, 'r') as f:
        content = f.read()
    current_paper = json.loads(content)
    current_paper['metadata'] = {'paper_id': current_paper['paper_id'], 'title': current_paper['metadata']['title']}
    del current_paper['paper_id']
    for word in unwanted:
        del current_paper[word]
    with open(path, 'w') as f:
        f.write(json.dumps(current_paper, indent=4, sort_keys=True))

