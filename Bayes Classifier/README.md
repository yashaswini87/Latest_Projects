homework_06
===========

This homework you will understand a naive bayes classifier, write an NLP tagging/feature extraction and then put the two together to classify the nltk movie reviews corpus (type: nltk.corpus.movie_reviews.readme() in your python shell to see more details about the dataset)

There are essentially 4 parts to this homework.

1) You will write code into a framework as in past homeworks; here you will fill in all the NLP, tagging functions in tagger.py Follow the in-line documentation.
2) You will read through and understand how the Naive Bayes classifier in classifier.py works. This will involve writing standard inline documenation (description, Paramaters, and Return where applicable).
3) You wrap classifier.py and tagger.py in main.py to classifiy a test_set from nltk.corpus.movie_reviews
4) You will prepare a 10min presentation to give in front of the class which will contain an explanation of the functions, code inter/inner-dependency, math background and results of your classifier. A randomly selected two teams will be asked to present on April 22nd.   

**Due:**  Monday April 22nd, 2013.

To receive full credit, you must commit and push code that passes all unit tests, write the in-line documentation and prepare the presentation. 

----

Setup
-----

Clone the repo and save it in a local directory called `homework_06` by typing

    git clone https://github.com/columbia-applied-data-science/homework_06_team_XX.git \
    homework_06


Package
-------
Note:  To use the `homework_06` package, your PYTHONPATH must be modified.  In your `~/.bashrc` (or `~/.bash_profile` on macs), put

    export PYTHONPATH=path-to-directory-above-homework_06:$PYTHONPATH

Then source it with `source ~/.bashrc` or open a new terminal.

* If you have any issues with this, see earlier README's for more details


The Code
--------

The code is broken up in to three parts:

1) classifier.py - This is the framework you will write the NaiveBayes classifier in. You are expected to create a configurable class that can be trained on input training datasets and then can be used to classify new input. For more details see the docstrings for the class and its methods.
2) tagger.py - This is a list of functions for tagging and extracting features; please see the in-function documentation for more details
3) main.py - This you can use to tie the whole process together - it is very open


Unit Tests
----------

To run tests, cd to *tests/* and do

    python -m unittest -v tagger_test

Once you are done, you will get notification that all tests passed.
