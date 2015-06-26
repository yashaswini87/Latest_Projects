import nltk
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from scripts.get_wpid import ProductGenome 
import urllib2
import pandas as pd
import json

nltk.download('http://nltk.org/data.html')
pos = 0
neg = 0
nouns_and_noun_phrases = []


servers = {"PROD": "kaos-cass00.sv.walmartlabs.com"}

def get_wmid(productid):
    pg = ProductGenome(server_url=servers.get("PROD"))
    wpid= pg.get_variant_wpids(productid)
    return wpid

def get_features(wpid):
    url='http://catalog.prod.cdqarth.prod.walmart.com/catalog-service/v0.3/catalog/products/search?filter=product_id=%s&tenantId=0' %wpid
    response=urllib2.urlopen(url, timeout=10)
    spell_json=json.load(response)
    features= spell_json['docs'][0]['product_attributes'].keys()
# features=["size","wetness indicator","absorb","quality","deliver","ship","offer","softness","weight","price"]
    for feature in features:
        feature_list=feature.split('_')
    return feature_list

def modify_features(feature_list):
    return feature_list

def feature_senti(reviewfile,feature_list,outputfile=None):
    feature_sent_dict={}
    for f in feature_list:
        f=f.lower()
        feature_sent_dict[f]={}
        feature_sent_dict[f]['pos']=0
        feature_sent_dict[f]['neg']=0
    with open(reviewfile,'r') as review_file:
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
                for feature in feature_sent_dict.keys():
                    if feature in sentence :
                        pol = sentence.sentiment.polarity 
                        if pol > 0:
                            feature_sent_dict[feature]['pos']+=1
                        
                        # print sentence
                        if pol < 0:
                            feature_sent_dict[feature]['neg']+=1
                        print sentence
                nouns_and_noun_phrases.append(' '.join(sentence_features["noun_phrases"] + sentence_features["nouns"]))
    cv = CountVectorizer(ngram_range=(1,2), min_df=0.01)
    cv.fit_transform(nouns_and_noun_phrases)
    return feature_sent_dict

def get_feature_senti(productid,reviewfile):
    wpid=get_wmid(productid)
    feature_list=get_features(wpid)
    feature_list=modify_features(feature_list)
    return feature_senti(reviewfile,feature_list)