# TruthGuard

TruthGuard is a Python NLP project that classifies COVID-19 news articles, separating evidence-based reporting from conspiracy theories. It’s built to help combat misinformation and promote reliable information during the pandemic.

## Demo

### Home Page
<p align="center">
  <img src="assets/home.png" alt="Home" style="max-width: 100%; width: 800px; height: auto;">
</p>

### Generating a Prediction using Article URL
<p align="center">
  <img src="assets/search-by-link.png" alt="Search by URL" style="max-width: 100%; width: 800px; height: auto;">
</p>
<p align="center">
  <img src="assets/search-by-link-results.png" alt="Results 1" style="max-width: 100%; width: 800px; height: auto;">
</p>

### Generating a Prediction from Article Text 
<p align="center">
  <img src="assets/search-by-text.png" alt="Search by Text" style="max-width: 100%; width: 800px; height: auto;">
</p>
<p align="center">
  <img src="assets/search-by-text-results.png" alt="Results 2" style="max-width: 100%; width: 800px; height: auto;">
</p>

source for text: [Reuters](https://www.reuters.com/business/healthcare-pharmaceuticals/do-i-need-worry-about-covid-again-2023-09-07/)

## Tools Used:
- pre-trained ''word2vec-google-news-300'' **Word2Vec** model: for generating meaningful word embeddings
- **Sci-kit Learn** Library: to train various machine learning models.
- **Spacy** package: utilized for advanced text processing.
- **Pandas** & **Matplotlib**: for data manipulation and visualization
- **Chart.js**: for visualizing prediction data
- **Regular Expressions**: for cleaning and preparing the textual data.
- **Beautiful Soup**: for intelligent parsing of web scrapage.
- **Newspaper3k** package: to extract complete news articles.

## Methodology
My journey started with identifying websites labeled as pro-science or conspiracy-themed using MediaBiasFactCheck. To gather data, I built a custom scraper with Beautiful Soup that pulled metadata from the latest COVID-19 articles on these sites.

Using Newspaper3k, I retrieved the full text of relevant articles. The data was then cleaned and refined with SpaCy and regular expressions—removing dates, links, stop words, and applying lemmatization to create a more analyzable dataset.

To capture the semantic meaning of each article, I applied the pre-trained Word2Vec Google News (300d) model, generating embeddings that reflected the nuanced language of news content.

Finally, I split the dataset into training and test sets and trained multiple machine learning models from Scikit-learn—including Logistic Regression, Support Vector Machine, Linear Discriminant Analysis, Naive Bayes, and Decision Tree Classifier. Each model was evaluated to identify the most effective approach for accurately classifying articles.TruthGuard stands as a testament to the power of combining advanced NLP techniques and machine learning to illuminate the truth in a world overwhelmed with misinformation.

