
import json
import os

for file in os.listdir('data'):
    with open('data/' + file, 'r') as f:
        content = str(f.read())
        json_str = json.loads(content)

# note, not considering 


# do some sort of validation to make sure all files have required keys with required features (or smth similar ofc)
