
next steps:
- make sure model initialization is good to go
- go over to model training and remove redundancies and add back models
- methods in notebooks and bagOfWords
    - add argument types and return type
    - add docstrings
- add supporting comments throughout notebooks
- finish writing write-up and add drawings and visualizations
- front-end deployment
- iron out terminology and variable names in bagOfWords.py
    - take a look at the vocabulary used 
    - 
- after all prerequisites are over, focus on extra stuff, like
    - data formatting
    - saving data to a cloud database and seeing if some sort of continuity is possible to automate model training based on a larger dataset
    - see if any more visualizations can be added, or if any that previously existed have accidentally been deleted
- further exploration
    - neural network stuff for nlp
    - evaluation for possibility of bag of words model literature review

questions:
- should I remove words with relative frequency equal to 0?
    - don't think it would make much of a difference anyway to start off with

issues:
- why is scientific vs conspiracy so unbalanced right now?
- need a lot of validation to fix bugs that didn't even know existed
    - best example is training and test dataframe issue