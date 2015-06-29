import collections
from collections import defaultdict
import nltk
import pdb



def document_features(document, tagger_output):
    """
    This function takes a document and a tagger_output=[(word,tag)]
    (see functions below), and tells you which words were present as
    'words' (as opposed to 'tags') in tagger_output.

    Parameters
    ----------
    document: string, your document
    tagger_output: list of tuples of the form [(word, tag)]
    
    Returns
    -------
    features : dictionary of tuples ('has(word)': Boolean)

    Notes
    -----
    Use the nltk.word_tokenize() to break up your text into words 
    """
    words = [word for (word,tag) in docTag(document)]    # break up text into words
    s = {word for (word,tag) in tagger_output}  # select word from the list of tuples
    bool_list =[(expression in words) for expression in s]   # True if words are present as word in tagger_output
    features = dict(zip(s,bool_list))  # form a dictionary of tuples   
    return features
    
def usefulDocumentFeatures(doc, dict):
    tagged_tokens = docTag(doc)
    words = []
    for tup in tagged_tokens:
        new_word = tup[0]
        try:
            if dict[new_word]:
                words.append(new_word)
        except KeyError:
            pass
    return words
                



def checkFeatures(document, feature_words):
    """
    This function takes a document and a list of feautures, i.e. words you
    have identitifed as features, and returns a dictionary telling you which
    words are in the document

    Parameters
    ----------
    document: list of strings (words in the text you are analyzing)
    features: list of strings (words in your feature list)

    Returns
    -------
    features: dictionary
        keys are Sting (the words)
        values are Boolean (True if word in feature_words)
    """ 
    bool_list = [x in document for x in feature_words]  # list of booleans to see presence of features
    features = dict(zip(feature_words,bool_list))  # form a dictionary
    return features





def onlyAlpha(document):
    """
    Takes a list of strings in your document and gets rid of everything that
    is not alpha, i.e. returns only words

    Parameters
    ----------
    document: list of strings

    Returns
    -------
    words: list of strings
    """
    words=[]

    for w in document:
        if w.isalpha():
            words.append(w)
    
    return words





def getTopWords(word_list, percent):
    """
    Takes a word list and returns the top percent of freq. of occurence.
    I.e. if percent = 0.3, then return the top 30% of word_list.
    
    Parameters
    ----------
    word_list: list of words
    percent: float in [0,1]

    Returns
    -------
    top_words: list 

    Notes
    -----
    Make sure this returns only alpha character strings, i.e. just words.
    Also, consider using the nltk.FreqDist()
    """
    ###get rid of non alphas in case you have any
    word_list = onlyAlpha(word_list)
    topwords=[]
    ## using nltk.FreqDist() to find the Frequency of words
    fdist = nltk.FreqDist(word.lower() for word in word_list)

    popular_words=sorted(fdist, key = fdist.get, reverse = True)

    topwords=popular_words[:(int(percent*len(popular_words))+1)]

    return topwords 




def posTagger(documents, pos_type=None, dummy_filter=False):
    """
    Takes a list of strings, i.e. your documents, and tags all the words in the
    string using the nltk.pos_tag().
    In addition if pos_type is not None the function will return only tuples
    (word, tag) tuples where tag is of type pos_type. For example, if
    pos_type = 'NN' we will get back all words tagged with "NN" "NNP" "NNS" etc

    Parameters
    ----------
    documents: list of strings
    pos_type: string

    Returns
    -------
    tagged_words: list of tuples (word, pos)

    Notes
    -----
    You need to turn each string in your documents list into a list of words and you want to return a list of unique (word, tag) tuples. Use the nltk.word_tokenize() to break up your text into words but MAKE SURE you return only alpha characters words
    """
    tagged_words = [] # Initialize empty list
    
    for document in documents:
        tokenized_doc = nltk.word_tokenize(document) # Tokenize the document
        taggedTokens = nltk.pos_tag(tokenized_doc) # Tag the tokens first 
        taggedTokens=[(a,b) for (a,b) in taggedTokens if a.isalpha()] #return only alpha character strings in the already tokened list     
        
        # Now, filter the tokens that don't fit pos_type
        # And convert to list of lists for bigramtagger
        maxLen = len(taggedTokens)
        if dummy_filter:

            toAdd = [taggedTokens[i][0] for i in range(0,maxLen) if taggedTokens[i][1] not in ['CC','RP','PRP','PRP$','TO','IN','LS','DT']] 
            #toAdd=set(toAdd)
        ##[list(x) for x in taggedTokens if x[1] == pos_type]
        
        elif pos_type is None:
            
            toAdd = [taggedTokens[i] for i in range(0,maxLen)]
            #toAdd=set(toAdd)

        else: 
            
            toAdd = [taggedTokens[i] for i in range(0,maxLen) if taggedTokens[i][1][:2]==pos_type[:2]] 

            
        tagged_words += (toAdd) # Add to list
    tagged_words=list(set(tagged_words))
    
    return tagged_words





def bigramTagger(train_data, docs_to_tag, base_tagger=posTagger, pos_type=None):
    """
    Takes a list of strings, i.e. your documents, trains a bigram tagger using the base_tagger for a first pass, then tags all the words in the documents. In addition if pos_type is not None the function will return only those (word, tag) tuples where tag is of type pos_type. For example, if pos_type = 'NN' we will get back all words tagged with "NN" "NNP" "NNS" etc

    Parameters
    ----------
    train_data: list of tuples (word, tag), for trainging the tagger
    docs_to_tag: list of strings, the documents you want to extract tags from
    pos_type: string

    Returns
    -------
    tagged_words: list of tuples (word, pos)

    Notes
    -----
    You need to turn each string in your documents list into a list of words and you want to return a list of unique (word, tag) tuples. Use the nltk.word_tokenize() to break up your text into words but MAKE SURE you return only alpha characters words. Also, note that nltk.bigramTagger() is touchy and doesn't like [(word,tag)] - you need to make this a list of lists, i.e. [[(word,tag)]]
    """
    ourTagger = nltk.BigramTagger(train_data, model=base_tagger)
    tagged_words = [] # Initialize empty list
    
    for document in docs_to_tag:
        
        taggedTokens = docTag(document)
        
        # Now, filter the tokens that don't fit pos_type
        # And convert to list of lists for bigramtagger
        if pos_type is None:
            
            toAdd = [taggedTokens[i] for i in range(0,len(taggedTokens))]
            #toAdd=set(toAdd)
        else:
        
            toAdd = [taggedTokens[i] for i in range(0,len(taggedTokens)) if taggedTokens[i][1][:2]==pos_type[:2]] 
            #toAdd=set(toAdd)
        ##[list(x) for x in taggedTokens if x[1] == pos_type]
            
        tagged_words += toAdd # Add to list
    tagged_words=set(tagged_words)

    return tagged_words

def docTag(document):
    """
    Takes a document and only returns the ONLY word tokens using onlyAlpha.
    
    Parameters:
    ----------
    doc: the document of interest
    
    Returns
    -------
    wordList: a list of word tokens.
    """
    
    tokenized_doc = nltk.word_tokenize(document)
    taggedTokens = nltk.pos_tag(tokenized_doc)
    
    return taggedTokens
    
    





    







