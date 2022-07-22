
import json
import os

for file in os.listdir('data'):
    path = 'data/' + file
    content = None
    with open(path, 'r') as f:
        content = f.read()
    current_paper = json.loads(content)
    # 
    abstract_text, body_text = '', ''
    for elem in current_paper['abstract']:
        abstract_text += elem['text']
    for elem in current_paper['body_text']:
        body_text += elem['text']
    abstract_text = abstract_text[:-1]
    body_text = body_text[:-1]
    del current_paper['abstract']
    del current_paper['body_text']
    current_paper['abstract_text'] = abstract_text
    current_paper['body_text'] = body_text
    # 
    with open(path, 'w') as f:
        f.write(json.dumps(current_paper, indent=4, sort_keys=True))

# note, not considering 


# do some sort of validation to make sure all files have required keys with required features (or smth similar ofc)
