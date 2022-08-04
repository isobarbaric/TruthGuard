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

things worked on:

things ongoing:

things going to be tried out:

