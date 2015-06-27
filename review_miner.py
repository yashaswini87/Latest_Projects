import nltk
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from scripts.get_wpid import ProductGenome 
import urllib2
import pandas as pd
import json
from nltk.corpus import stopwords
# from scripts import get_reviews

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
                        if len(f)>1:
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

def get_feature_senti(productid, get_reviews=False):
    review_file = './reviews/reviews_{}.txt'.format(productid)
    if get_reviews:
        review_file = './reviews/reviews_{}.txt'.format(productid)
        get_reviews.get_reviews(productid,review_file)
    wpid=get_wmid(productid)
    wpid=str(wpid.pop())
    feature_list=get_features(wpid)
    feature_list=modify_features(feature_list)
    outputfile='./reviews/sentiment_%s.txt' %productid
    return feature_senti(review_file,feature_list,outputfile=outputfile)

if __name__=='__main__':
    product_id = '35121100'
    selected_features = {}
    feature_name_mapping = {"rate" : "refresh rate", "ship" : "shipping", "deliver": "shipping","remote":"remote control","control":"remote control"}
    selected_features['35121100'] = ['height', 'weight', 'length', 'color', 'fabric', 'instructions', 'brand', 'assembled', 'price', 'ship']
    selected_features['34390987'] = ['height', 'weight', 'brand', 'assembled', 'price', 'ship']
    selected_features['25059351']=['price','quality','screen','brand','remote','control','rate','weight','resolution','warranty','ship','deliver']
    feature_info = get_feature_senti(product_id)
    review_summary = {"product_id": product_id}
    data = []
    series = [{"name": "Positive", "data": []}, {"name": "Negative", "data": []}]
    categories = []
    for feat_info in feature_info.iterkeys():
        name = feat_info
        d = feature_info[feat_info]
        pos = d["pos"]
        neg = d["neg"]
        if feat_info in selected_features[product_id]:
            name=name if name not in feature_name_mapping else feature_name_mapping[name]
            data_point = {}
            data_point["name"] = name 
            data_point['y'] = pos + neg
            data.append(data_point)
            categories.append(name.title())
            series[0]["data"].append(pos)
            series[1]["data"].append(neg)
    review_summary["data"] = data
    review_summary["col_data"] = series
    review_summary["col_cats"] = categories

with open("new_review_data.txt", 'a') as review_data_file:
    review_data_file.write(json.dumps(review_summary) + '\n')
#     get_feature_senti('28240450','./reviews/reviews_diapers_28240450.txt')