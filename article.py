
import json
import os

unwanted = ['back_matter', 'bib_entries', 'ref_entries']

for file in os.listdir('data'):
    print(file)
    with open('data/' + file, 'r+') as f:
        content = f.read()
        current_paper = json.loads(content)
        current_paper['metadata'] = {'paper_id': current_paper['paper_id'], 'title': current_paper['metadata']['title']}
        del current_paper['paper_id']
        for word in unwanted:
            del current_paper[word]
        f.seek(0)
        f.write(json.dumps(current_paper, indent=4, sort_keys=True))

# keys to drop: back_matter, bib_entries, ref_entries
# keys to format, take meta_data and replace with key just containing its title attribute
