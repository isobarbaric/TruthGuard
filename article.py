
import os
import json

# file_data = open('data/article-108.json', 'w')
# file_data.write(json.dumps(file_data, indent=4, sort_keys=True))

files = sorted(os.listdir('data'), key=lambda x: int(x[x.find('-')+1:x.find('.')]))


for file in files:
    print(file)
    with open('data/' + file, 'r+') as storage:
        a = storage.read()
        parsed = json.loads(a)
        storage.seek(0)
        storage.write(json.dumps(parsed, indent = 4, sort_keys=True))


