
this version is more updated than the google docs one 

next steps:
DONE => make sure model initialization is good to go 
SKIPPING FOR NOW => go over to model training and remove redundancies and add back models (here rn)
    - look through other models that can be tried out
    - go over existing models and review ways to make them more accurate (analyze classification report to see where there is room for improvement)
    - see if can add models to a list and then select model with highest accuracy
RIGHT NOW => methods in notebooks and bagOfWords
- make it so that all variables used throughout are declared in the __init__

    - add argument types and return type
    - add docstrings

make modifications before docstrings
make final changes to docstrings

- add supporting comments throughout notebooks
- finish writing write-up and add drawings and visualizations
- front-end deployment
- iron out terminology and variable names in bagOfWords.py
    - take a look at the vocabulary used 
    - research proper terminology and order and adjust accordingly
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
- other things to fine-tune
    - includes parameters manually controlled; things like
        - number of relevant words chosen

to add:
- consider adding sklearn make_pipeline in the midst

to do:
=> add docstrings, comments to notebook and bag_of_words
=> 

add data types and return types to functions in notebooks

remove 'text' from article dictionary in data_acquitision (make sure testing works for data_processing in the future)

add headers in 