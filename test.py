
import nltk
from nltk.stem import WordNetLemmatizer

# some inaccuracies, 'typed' returns noun?
def getPartOfSpeech(provided_word): 
    _, part_of_speech = nltk.pos_tag([provided_word])[0]
    print(part_of_speech)

    if 'NN' in part_of_speech:
        return 'n'
    elif 'VB' in part_of_speech:
        return 'v'
    elif 'JJ' in part_of_speech:
        return 'a'
    elif 'RB' in part_of_speech:
        return 'r'

    return 'n'

lemmatizer = WordNetLemmatizer()

print(lemmatizer.lemmatize('typing', getPartOfSpeech('typing')))


