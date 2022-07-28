
import json
from sklearn.model_selection import train_test_split


class DataModel:

    def __init__(self, min_len_enforced=True):
        self.min_len_enforced = min_len_enforced
        self.load_articles()

    def load_articles(self):
        self.scientific_articles = []
        with open('json/science.json', 'r') as storage:
            info = json.loads(storage.read())
            for article in info:
                self.scientific_articles.append(article[1])

        self.conspiracy_articles = [] 
        with open('json/conspiracy.json', 'r') as storage:
            info = json.loads(storage.read())
            for article in info:
                self.conspiracy_articles.append(article[1])

        print(len(scientific_articles), len(conspiracy_articles))

        if self.min_len_enforced:
            min_len = min(len(scientific_articles), len(conspiracy_articles))
            scientific_articles = scientific_articles[:min_len]
            conspiracy_articles = conspiracy_articles[:min_len]

    def split_data(self):
        self.training_science_set, self.test_science_set = train_test_split(scientific_articles, test_size = 0.2, random_state = 1)
        self.training_conspiracy_set, test_conspiracy_set = train_test_split(conspiracy_articles, test_size = 0.2, random_state = 1)
        training_set = self.training_science_set + self.training_conspiracy_set
        test_set = self.test_science_set + self.test_conspiracy_set



# # %%
# len(training_set)

# # %%
# len(test_set)

# # %%
# from nltk import word_tokenize
# from nltk.corpus import stopwords
# from dateutil.parser import parse
# from nltk.stem import WordNetLemmatizer
# import matplotlib.pyplot as plt

# import string
# import nltk

# class BagOfWords:
#     def __init__(self, tokenized_paragraph: list, is_positive: bool):
#         self.sentences = tokenized_paragraph
#         self.is_positive = is_positive

#     def tokenize(self):
#         self.words = []
#         for sentence in self.sentences:
#             for word in word_tokenize(sentence):
#                 self.words.append(word)

#     def to_lower_case(self):
#         for i in range(len(self.words)):
#             self.words[i] = self.words[i].lower()

#     def clean_data(self):
#         noise = ['...', "n't"]
#         def is_time_or_date(word):  
#             try:
#                 parsed = parse(word)
#                 return True
#             except:
#                 return False

#         def is_link(word):
#             suffixes = ['.com', '.org', '.edu', '.gov', '.int', '.co', '.net', '.au', '.us', '.uk', '.ne', 'news']
#             for suffix in suffixes:
#                 if suffix in word:
#                     return True
#             return False

#         for i in range(len(self.words)-1, -1, -1):
#             if len(self.words[i]) <= 2 or self.words[i].isnumeric() or is_time_or_date(self.words[i]) or self.words[i] in noise or is_link(self.words[i]) or self.words[i] in [letter for letter in string.ascii_lowercase]:
#                 self.words.pop(i)
#                 continue
        
#             # shave punctation off of beginnings and from the end
#             start_ind, end_ind = -1, -1
#             for j in range(len(self.words[i])):
#                 if self.words[i][j] in string.ascii_lowercase or self.words[i][j].isnumeric():
#                     start_ind = j
#                     break
#             for j in range(len(self.words[i])-1, -1, -1):
#                 if self.words[i][j] in string.ascii_lowercase or self.words[i][j].isnumeric():
#                     end_ind = j
#                     break

#             if (start_ind == 0 and end_ind == len(self.words[i])-1) or start_ind >= end_ind:
#                 continue

#             self.words[i] = self.words[i][start_ind:end_ind+1]

#     def remove_stop_words(self):
#         for i in range(len(self.words)-1, -1, -1):
#             if self.words[i] in stopwords.words('english'):
#                 self.words.pop(i)  

#     def normalize_words(self):
#         def get_part_of_speech(provided_word):
#             _, part_of_speech = nltk.pos_tag([provided_word])[0]
#             if 'NN' in part_of_speech:
#                 return 'n'
#             if 'VB' in part_of_speech:
#                 return 'v'
#             if 'JJ' in part_of_speech:
#                 return 'a'
#             if 'RB' in part_of_speech:
#                 return 'r'
#             return 'n'

#         lemmatizer = WordNetLemmatizer()
#         for i in range(len(self.words)):
#             # if lemmatizer.lemmatize(self.words[i], get_part_of_speech(self.words[i])) == 'm':
#             #     print(self.words[i])
#             self.words[i] = lemmatizer.lemmatize(self.words[i], get_part_of_speech(self.words[i]))

#         # perform some data cleaning on lemmatized words
#         for i in range(len(self.words)-1, -1, -1):
#             if self.words[i] in [letter for letter in string.ascii_lowercase]:
#                 self.words.pop(i)  

#     def create_frequency_chart(self):
#         self.freqChart = dict()

#         for word in self.words:
#             if word not in self.freqChart:
#                 self.freqChart[word] = 1
#             else:
#                 self.freqChart[word] += 1

#         # sorting in ascending order by value
#         self.freqChart = {word: self.freqChart[word] for word in sorted(self.freqChart, key=self.freqChart.get, reverse=True)}

#     def plot_frequency_chart(self):
#         words = list(self.freqChart.keys())[:100]
#         frequencies = list(self.freqChart.values())[:100]

#         plt.figure(figsize=(20, 5))
#         plt.margins(x=0, tight=True)
#         plt.bar(words, frequencies, color ='green')

#         # setting title and labels
#         plt.xlabel("Distinct Words")
#         plt.tick_params(axis='x', which='major', labelsize=9)
#         plt.xticks(rotation = 90)

#         plt.ylabel(f"Frequency of Words in {self.is_positive}")
#         plt.title("Frequency Chart")

#         # loading the plot
#         plt.show()

# # %%
# science_train = BagOfWords(training_science_set, True)

# science_train.tokenize()
# science_train.to_lower_case()
# science_train.clean_data()
# science_train.remove_stop_words()
# science_train.normalize_words() # todo: improve part of speech performance
# science_train.create_frequency_chart()
# science_train.plot_frequency_chart()

# # %%
# conspiracy_train = BagOfWords(training_conspiracy_set, False)

# # assuming rn that everything is clean because of testing on 'a', will test later
# conspiracy_train.tokenize()
# conspiracy_train.to_lower_case()
# conspiracy_train.clean_data()
# conspiracy_train.remove_stop_words()
# conspiracy_train.normalize_words() # todo: improve part of speech performance
# conspiracy_train.create_frequency_chart()
# conspiracy_train.plot_frequency_chart()

# # %%
# science_test = BagOfWords(test_science_set, True)

# science_test.tokenize()
# science_test.to_lower_case()
# science_test.clean_data()
# science_test.remove_stop_words()
# science_test.normalize_words() # todo: improve part of speech performance
# science_test.create_frequency_chart()
# # plotting frequency is not relevant for test set

# # %%
# conspiracy_test = BagOfWords(test_conspiracy_set, False)

# conspiracy_test.tokenize()
# conspiracy_test.to_lower_case()
# conspiracy_test.clean_data()
# conspiracy_test.remove_stop_words()
# conspiracy_test.normalize_words() # todo: improve part of speech performance
# conspiracy_test.create_frequency_chart()
# # plotting frequency is not relevant for test set

# # %%
# def get_common_words(a: BagOfWords, b: BagOfWords):
#     # determine common words between the two sets of words
#     common_words = dict()
#     for word, count in a.freqChart.items():
#         if word in b.freqChart:
#             diff_count = count - b.freqChart[word]
#             common_words[word] = diff_count/(count + b.freqChart[word])

#     # remove all with count 0 
#     common_words = dict(filter(lambda elem: elem[1] != 0, common_words.items()))

#     # sorting the dictionary in descending order
#     common_words = {word: common_words[word] for word in sorted(common_words, key=common_words.get, reverse=True)}

#     return common_words

# # %%
# train_common_words = get_common_words(science_train, conspiracy_train)

# # %%
# train_common_words

# # %%
# def get_stats_common_words(common_words):
#     print(len(common_words), sep = ', ')
#     print(sum(y > 0 for _, y in common_words.items()))
#     print(sum(y < 0 for _, y in common_words.items()))

# # %%
# get_stats_common_words(train_common_words)

# # %%
# def get_relevant_words(common_words, num_words = 500):
#     # extract 20 most common words
#     sorted_words = []
#     for key, value in common_words.items():
#         sorted_words.append([abs(value), key])
#     sorted_words.sort(reverse=True)

#     # take 20 with highest magnitudes  
#     relevant_words = sorted_words[:num_words]

#     # give the sign back
#     for word in relevant_words:
#         word[0] = common_words[word[1]]

#     relevant_words.sort()
#     return relevant_words

# # %%
# train_relevant_words = get_relevant_words(train_common_words, 200)

# # %%
# train_relevant_words

# # %% [markdown]
# # - split up data into testing, training set
# #     - in an 80-20 split
# #     - do this individually for scientific articles and conspiracy articles, then merge the two sets together
# # - after this, evaluation of well the system works with a ML model will be good
# #     - train model and redo-word frequency part once for the testing set and once for the training set (to prevent data leakage)
# #     - generate table for training and testing data (2 tables)
# #         - columns: for each of the 20 keywords
# #         - rows: count for each keyword in an article  
# #         - add a final column to the right displaying whether the article was a conspiracy or scientific (0 = conspiracy, 1 = scientific) 
# #     - train model with various different methods and evaluate test set  

# # %%
# import pandas as pd
# import numpy as np

# # build the dataframe
# def build_training_dataframe(relevant_words):
#     cols = {}
#     for word in relevant_words:
#         cols[word[1]] = []

#     # adding scientific rows
#     for article in training_science_set:
#         for word in cols:
#             cols[word].append(article.lower().count(word))

#     # adding conspiracy row
#     for article in training_conspiracy_set:
#         for word in cols:
#             cols[word].append(article.lower().count(word))

#     data_set = pd.DataFrame(data = cols)

#     row_count = data_set.shape[0]/2

#     # setting scientific articles to 1
#     data_set.loc[:row_count,'article_type'] = 1

#     # setting conspiracy articles to 0
#     data_set.loc[row_count:, 'article_type'] = 0

#     return data_set

# # %%
# train_data = build_training_dataframe(train_relevant_words)

# # %%
# def build_test_dataframe(train_relevant_words):
#     cols = {}
#     for word in train_relevant_words:
#         cols[word[1]] = []

#     # adding scientific rows
#     for article in test_science_set:
#         for word in cols:
#             cols[word].append(article.lower().count(word))

#     # adding conspiracy row
#     for article in test_conspiracy_set:
#         for word in cols:
#             cols[word].append(article.lower().count(word))

#     data_set = pd.DataFrame(data = cols)

#     row_count = data_set.shape[0]/2

#     # setting scientific articles to 1
#     data_set.loc[:row_count,'article_type'] = 1

#     # setting conspiracy articles to 0
#     data_set.loc[row_count:, 'article_type'] = 0

#     return data_set

# # %%
# test_data = build_test_dataframe(train_relevant_words)

# # %%
# def no_elem_check(data_set):
#     # make sure no columns have 0s for all the rows, should be true
#     for col in data_set:
#         unique_elem = data_set[col].unique()
#         if len(unique_elem) == 0 and unique_elem[0] == 0:
#             print(col)

# # %%
# train_data.columns

# # %%
# train_data

# # %%
# test_data

# # %%
# # get unique elements in column
# def get_unique_col(data_set, col_name):
#     return data_set[col_name].unique()

# # get unique elements in column but for only those with a certain feature 
# def get_unique_col(data_set, col_name, article_type):
#     return data_set[data_set['article_type'] == article_type][col_name].unique()

# # %%
# get_unique_col(train_data, 'mainstream', 0)

# # %%
# X_train = train_data.iloc[:, :-1]
# y_train = train_data.iloc[:, -1]

# # %%
# X_train

# # %%
# y_train

# # %%
# X_test = test_data.iloc[:, :-1]
# y_test = test_data.iloc[:, -1]

# # %%
# def get_frequency(data_set):
#     return (data_set != 1).values.sum()/len(data_set) * 100

# print(get_frequency(y_train))
# print(get_frequency(y_test))

# # %%
# # logistic regression
# from sklearn.linear_model import LogisticRegression
# lg_model = LogisticRegression(random_state = 1, max_iter = 10000)

# lg_model.fit(X_train, y_train)
# lg_pred = lg_model.predict(X_test)

# # %%
# # linear discriminant analysis
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# lda_model = LinearDiscriminantAnalysis()

# lda_model.fit(X_train, y_train)
# lda_pred = lda_model.predict(X_test)

# # %%
# # k-nearest neighbors
# from sklearn.neighbors import KNeighborsClassifier
# knn_model = KNeighborsClassifier(n_neighbors=15)

# knn_model.fit(X_train, y_train)
# knn_pred = knn_model.predict(X_test)

# # %%
# # naive-bayes
# from sklearn.naive_bayes import GaussianNB
# nb_model = GaussianNB()

# nb_model.fit(X_train, y_train)
# nb_pred = nb_model.predict(X_test)

# # %%
# # decision tree
# from sklearn.tree import DecisionTreeClassifier
# dt_model = DecisionTreeClassifier(random_state = 1)

# dt_model.fit(X_train, y_train)
# dt_pred = dt_model.predict(X_test)

# # %%
# # support-vector machine
# from sklearn.svm import SVC
# svc_model = SVC(kernel = 'linear',gamma = 'scale', shrinking = False)

# svc_model.fit(X_train, y_train)
# svc_pred = svc_model.predict(X_test)

# # %%
# from sklearn.metrics import accuracy_score, f1_score, classification_report

# # %%
# print(classification_report(y_test, lg_pred))

# # %%
# print(classification_report(y_test, lda_pred))

# # %%
# print(classification_report(y_test, knn_pred))

# # %%
# print(classification_report(y_test, nb_pred))

# # %%
# print(classification_report(y_test, dt_pred))

# # %%
# print(classification_report(y_test, svc_pred))


