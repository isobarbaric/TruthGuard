# COVID19-Classifier

## Methodology

![Pipeline Steps](images/methodology.png)

<center>pipeline steps</center>

### Data Acquisition

To create a bag of words model and train it, it is necessary to have labeled data. As data in this context would be the textual content in news articles (of various sources), identifying these labels on their own is not a trivial task. Adding to this, as there is a lot of data to gather and frequently, individually classifying articles manually would not be feasible. Thus, being able to classify an article without human intervention is a necessity.

An approach to do exactly this is to use MediaBiasFactCheck's categorization of scientific and conspiracy sources, specifically with the 'Pro-Science' and 'Conspiracy-Pseudoscience' categories. This approach assumes that websites of a specific category can be relied on to consistently produce articles that belong to that category. Performing basic web-scraping and obtaining two lists of articles from [MediaBiasFactCheck's website](https://mediabiasfactcheck.com/) provides a starting point to develop a database for articles of both kinds.

Now, given two lists of website URLs, with some advanced scraping, individual articles from these websites can be found and subsequently stored in a database. Specifically, the particular set of steps discussed so far (scraping for a single type of source on MBFC, finding articles from the URLs for that source), are facilitated by the ['ArticleFinder' class](https://github.com/isobarbaric/Fake-News-Classifier/blob/master/Pipeline/article_finder.py), which scrapes the home page and uses pattern recognition to locate all articles posted on a website's home page. Of all of the articles found, the title of the articles is matched with certain COVID-related keywords to determine its relevance to COVID-19. Subsequently, given the address to the articles and knowing possessing the label, the only thing left to do is obtain the text contents for those articles.

Obtaining the text contents is handled by the next step in the pipeline, data processing.

### Data Processing

Using the data gathered in the previous step, the goal of this section is to finalize that data - obtaining the texts for the articles - and format this data in order to pass it onto the next step in an appropriate format.

First and foremost and as aforementioned in the previous section, given all of the articles (their titles and links), the textual content of these articles needs to be obtained. For this specific use-case, the 'Article' class from the 'newspaper3k' library provides the exact functionality required. Given a URL, this class is able to return the text content for that article, which is exactly what is needed. Utilizing the 'download()' and 'parse()' methods, the text for a particular article is stored alongside the original data that was found earlier in the previous step, namely the title and link. As a result, the need to obtain the textual content for all of the articles is satisfied.

Secondly, this data needs to be stored in a format conducive to further analysis. The data is converted to a pandas DataFrame for ease of manipulation and notably, since this data is provided in two separate instances for the two classes (science and conspiracy), an extra column denoting their 'article_type' as a boolean is added to combine the two sets into one. With this and the subsequent text-retrieval described in the previous, a thorough DataFrame is built with columns 'title', 'link', 'text' and 'article_type'.

This DataFrame, combined with the text retrieved, can now be used in the next step in the pipeline.

## Aside: Bag of Words Model

As computers understand numbers, to process any natural language and be able to understand underlying patterns, it is necessary to - in some shape or form - convert the language we have into numbers. With this in mind, a bag of words model's approach to this is to use the frequency that a particular word occurs as its heuristic. So, given a body of text and a known vocabulary, the bag of words model can build an entire row of data based on the count of the word in the current column in the text. Once this extends beyond one row, it is possible to generate an entire matrix with the columns representing the words in the vocabulary and the rows representing individual articles, as relevant in this specific use-case.

To get to a stage where the count of a word can be found, there are 6 main intermediary steps that must be taken first.

1. Tokenization - ‘BagOfWords.tokenize()’
This is the process of splitting up paragraphs and sentences into smaller chunks. As we are interested in individually identifying all of the words in a body of text, the ‘BagOfWords.tokenize()’ utilizes word_tokenize from the nltk library to facilitate this.

2. Conversion to Lowercase - ‘BagOfWords.to_lower_case()’
Converting all of the words to a standard case is important so that a difference in case is not picked up as a difference in meaning. The same word can have multiple different cases in the same body of text and so standardization of the case is necessary. Effectively, converting all of the words to uppercase would produce an identical effect, but for stylistic reasons, lowercase is preferred.

3. Text Cleaning - ‘BagOfWords.clean_data()’
After all of the words have been separated and converted to their lowercase form, these words must now be checked and pruned of any unwanted content. Specifically, many words may contain punctuation in a certain prefix and suffix of the word, with this being an aftermath of being 

4. Removing Stop Words - ‘BagOfWords.remove_stop_words()’
Of the words in the refined vocabulary, there will be many words that occur very frequently but add little to the overall meaning being conveyed. For example, the words ‘the’ and ‘and’ may appear frequently but do not add any extra meaning specific to the subject matter. Such words are known as stop words. All such words are removed using a list of stopwords from ‘nltk.corpus’.

5. Lemmatization - ‘BagOfWords.lemmatize_words()’

Lemmatization is the process of converting a word to its base form. How exactly this works for a word depends on its part of speech, and on that basis, the word is changed. For example, the word ‘cats’, which is a noun, would be lemmatized to the word ‘cat’. On the other hand, the word ‘running’, which is a verb, would be lemmatized to ‘run’ (infinitive form of the verb). This process is important so that a difference in the form a specific word occurs does not go down as a difference in the meaning. Referring to the previous example, the word ‘cats’ and ‘cat’ convey a similar meaning, but appear as different words.

The ‘WordNetLemmatizer’ class from ‘nltk.stem’ combined with part of speech tagging with

6. Tabulating Frequency - ‘BagOfWords.create_frequency_chart()’’

Now that all of the data has been thoroughly processed, the final step towards the objective of getting the count for each word is just to count all of the words up. This can be done efficiently using a hash table, which in Python, would be a dictionary.

## Aside (cont.): Choice of Words for Bag of Words Model

![sample word distribution](images/freq_chart1.png)

<center>sample word distribution</center>

The relevance score for a particular word is defined as follows:

$$\text{relevance score}=\frac{\text{num of occurrences in scientific articles - num of  occurrences in conspiracy articles}}{\text{num of occurrences in scientific articles + num of  occurrences in conspiracy articles}}$$

Based on this heuristic, all of the words that are common to both BagOfWords objects are given a relevance score for assessment. Then, based on the scores all of these words attain, a certain top chunk of them can be retrieved based on magnitude to serve as words for the model.

To demonstrate such a process, below is a sample plot of what this looks like:

![sample relevance plot](images/freq_chart2.png)
<center>sample relevance plot</center>

# Conclusion

## Implications

As a proof of concept, the results we got definitively show that there is a distinction between scientific and conspiracy articles and that classification is possible. While the results obtained may not seem too accurate or precise, these results can definitely be used to provide suggestions on what category content may fall into.

An application for these results have a wide variety of applications such as tagging potentially unscientific information, a functionality similar to Twitter’s current misinformation banners. The utility of these results can be used in many domains, and can improve efficiency where classification is required on a massive scale. In such scenarios, models trained as in this project would massively help alleviate pressure by providing classification results on their own.

## Next Steps

Firstly, results would be improved with the current bag of words model if the selection criteria for the words in the vocabulary were more narrow. Optimizing hyperparameters is within the scope of this project, however, modifying the number of words and testing on that basis is incredibly difficult. Perhaps, a new utility class to assist with this is necessary, and such options will be explored. However, what is clear is that a more refined selection of words would improve model results.

Secondly, one aspect that would definitely help improve the model would be to increase the amount of data available to it. Such scaling is possible with the newspaper3k's ‘newspaper’ class, however, was not used for this project due to computational constraints. The number of articles obtained in such a scenario would be far too many to realistically be able to process, both in terms of time and memory. Perhaps, in a bid to remedy this, the complete list of potential URLs from MediaBiasFactCheck can be broken down into chunks and the chunks scraped to be stored on the cloud incrementally. Scaling with this functionality would provide access to a lot more data, which in turn, would massively improve results.

Finally, to further improve the initial goal of classification, more sophisticated models can be adapted in place of the current bag of words model, such as TF-IDF. Specifically, I am interested in using deep learning techniques to enhance performance as I think that will both be a great learning experience and will help generate better outcomes.