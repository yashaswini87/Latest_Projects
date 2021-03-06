# creating the features
def gender_class(word):
    return{'last_letter:word[-1]'}

# 
from nltk.corpus import names
import random
names=([(name,'male') for name in names.words('male.txt')]+[(name,'female'	) for name in names.words('female.txt')])
random.shuffle(names)
featuresets=[(gender_features(n),g) for (n,g) in names]
train_set,test_set=featuresets[500:],featuresets[:500]
classifier=nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier,test_set)
