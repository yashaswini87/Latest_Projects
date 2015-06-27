import nltk
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from scripts.get_wpid import ProductGenome 
import urllib2
import pandas as pd
import json
from nltk.corpus import stopwords
from scripts import get_reviews

nltk.download('http://nltk.org/data.html')
pos = 0
neg = 0
nouns_and_noun_phrases = []
# nltk.download()
ATTRS_TO_IGNORE=['actual_color','features','item_master_created_date','product_url_text','product_segment','type','alternate_shelves','item_type','gtin',
                 'product_category','walmart_department_number','category','wmt_category','model','upc','wupc','walmart_item_number',
                 'item_id','brand_code','wmt_category','product_type']
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
    feature_list=["ship", "price","size","quality","deliver","store"]
    for feature in features:
        feature_list.extend(feature.split('_'))
    return list(set(feature_list))

def modify_features(feature_list):
    new_feature_list=[]
    stop = stopwords.words('english')
    for f in feature_list:
        if f not in ATTRS_TO_IGNORE:
            if f not in stop:
                if 'id' not in f:
                    if 'path' not in f:
                        new_feature_list.append(f)
    return new_feature_list

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
    df=pd.DataFrame.from_dict(feature_sent_dict, orient='index').reset_index()
    df.cols=['feature','neg','pos']
    df.sort(['pos','neg'],ascending=[False,False],inplace=True)
    df.to_csv(outputfile)
    return feature_sent_dict

def get_feature_senti(productid,reviewfile):
#     reviewfile=get_reviews.get_reviews(productid)
    wpid=get_wmid(productid)
    wpid=str(wpid.pop())
    feature_list=get_features(wpid)
    feature_list=modify_features(feature_list)
    outputfile='./reviews/sentiment_%s.txt' %productid
    return feature_senti(reviewfile,feature_list,outputfile=outputfile)

if __name__=='__main__':
    get_feature_senti('4408441','./reviews/reviews_bed_4408441.txt')
#     get_feature_senti('28240450','./reviews/reviews_diapers_28240450.txt')