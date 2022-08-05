use bagOfWord's tokenizing when building dataframes maybe

first step: put all of the confusion matrices
get classification report to html
put stuff together in one table together

second step: use ConfusionMatrixDisplay class to stitch everything together

- correct/update confusion matrix contents before presenting tomorrow
- change headers from ['positive', 'negative'] to ['science', 'conspiracy']
 

=> updates to existing stuff
- update labels in table
- finish RandomizedSearchCV for the remaining models 
- make a predict method that returns a string and confidence level
=> deploy on flask server
=> report (docs + LaTeX)
=> add different sections for proj (like this: https://github.com/Fryingpannn/WallStreetBets_BigDataAnalysis)
- data
- preprocessing
    - proper code
    - commenting
- model training
- deployment
=> more experimentation

get the jargon going

- parameters to vary inside the model
    - model-specific: 
        - hyperparameters on current model and create blackbox-able structure
        - GridSearchCV, RandomizedGridSearchCV
    - heuristic-specific: 
        - number of articles
        - test_size
        - number of relevant words
    - more models
        - RandomForestClassifier
        - Gradient Processing
        - AdaBoost
        - ExtraTrees 
        - RidgeClassifier 
- try using libraries to compare model accuracy
    - scikit-learn CountVectorizer
    - spaCy
    - TextBlob 
- data source (CORD-19) and another potential source for the conspiracy articles

add features like, 
- paste article
- paste URL

