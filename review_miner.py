import nltk
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
nltk.download('http://nltk.org/data.html')
pos = 0
neg = 0
nouns_and_noun_phrases = []


import urllib2
import json
quoted_key='1EOLVBF5QVVT'
url='http://catalog.prod.cdqarth.prod.walmart.com/catalog-service/v0.3/catalog/products/search?filter=product_id=%s&tenantId=0' %quoted_key
response=urllib2.urlopen(url, timeout=10)
spell_json=json.load(response)
features= spell_json['docs'][0]['product_attributes'].keys()
# features=["size","wetness indicator","absorb","quality","deliver","ship","offer","softness","weight","price"]
    
feature_sent_dict={}
for feature in features:
    feature_list=feature.split('_')
    for f in feature_list:
        feature_sent_dict[f]={}
        feature_sent_dict[f]['pos']=0
        feature_sent_dict[f]['neg']=0
    
with open("./reviews/reviews_diapers_28240450.txt") as review_file:
    for line in review_file:
        review = line.strip()
        review_blob = TextBlob(review)
        for sentence in review_blob.sentences:
            sentence_features = {}
            sentence_features["sentence"] = sentence
            sentence_features["polarity"] = sentence.sentiment.polarity
            sentence_features["subjectivity"] = sentence.sentiment.subjectivity
            sentence_features["noun_phrases"] = sentence.noun_phrases
            sentence_features["nouns"] = []
            for token, tag in sentence.tags:
                if 'NN' in tag:
                    sentence_features["nouns"].append(token)
            for feature in features:
                if feature in sentence :
                    pol = sentence.sentiment.polarity 
                    if pol > 0:
                        feature_sent_dict[feature]['pos']+=1
                    
                    # print sentence
                    if pol < 0:
                        feature_sent_dict[feature]['neg']+=1
                    print sentence
            nouns_and_noun_phrases.append(' '.join(sentence_features["noun_phrases"] + sentence_features["nouns"]))
# 
# print "Positive", pos
# print "Negative", neg
print feature_sent_dict
cv = CountVectorizer(ngram_range=(1,2), min_df=0.01)
cv.fit_transform(nouns_and_noun_phrases)
