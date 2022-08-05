general parameters to vary

objective is to have data_model take parameters to vary the general parameters


make sure the use for each variable created is known
- can remove variables that are never used 

multiple changes to see how accuracy improves
- parameters to vary inside the model
    - model-specific: 
        - hyperparameters on current model and create blackbox-able structure
        - GridSearchCV, RandomizedGridSearchCV
    - heuristic-specific: 
        - number of articles
        - test_size
        - number of relevant words
- try using libraries to compare model accuracy
    - scikit-learn CountVectorizer
    - spaCy
    - TextBlob 
- data source (CORD-19) and another potential source for the conspiracy articles

-----

logistic regression:
- https://towardsdatascience.com/logistic-regression-model-tuning-with-scikit-learn-part-1-425142e01af5
- MiniMax Scaler



things worked on:
- predict method

things ongoing:
- 

things going to be tried out:
- 


first step: put all of the confusion matrices
get classification report to html
put stuff together in one table together

second step: use ConfusionMatrixDisplay class to stitch everything together

- review confusion matrix contents before presenting tomorrow
- change headers from ['positive', 'negative'] to ['science', 'conspiracy']