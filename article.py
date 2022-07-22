
import os

for count, value in enumerate(os.listdir('data')):
    os.rename('data/' + value, 'data/article-' + str(count+1) + '.json')
    print(count, value)
