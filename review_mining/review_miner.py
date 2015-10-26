from textblob import TextBlob
from scripts.get_wpid import ProductGenome 
import urllib2
import pandas as pd
import json
from nltk.corpus import stopwords
import sentence_clustering 
from random import randint
import wordcloud
from scripts import get_reviews
import review_demographics

selected_features = {}
feature_name_mapping = {"rate" : "refresh rate", "ship" : "shipping", "deliver": "shipping","remote":"remote control","control":"remote control"}

selected_features['35121100'] = ['height', 'weight', 'length', 'color', 'fabric', 'warrant','instructions', 'brand', 'assembled', 'price','ship','deliver']
selected_features['34390987'] = ['height', 'weight', 'brand', 'assembled', 'price', 'ship','warrant','price','ship','deliver']
selected_features['25059351']=['price','quality','screen','brand','rate','weight','resolution','warranty','ship','deliver','remote control']
selected_features['4408441']=['quality','finish','price','ship','wood','deliver','store','size','material','color','warrant','ship','deliver']
selected_features['29010048']=['screen', 'display','battery','camera','video','service','reception','warrant','price','ship','deliver']

product_url={}
product_url['4408441']='http://ll-us-i5.wal.co/dfw/dce07b8c-57c8/k2-_9398b44d-9567-4beb-841a-53b5c07fd15e.v2.jpg-1a0eb0d389b6f23a8747c7515812d495636fbe53-webp-450x450.webp'
product_url['25059351']='http://ll-us-i5.wal.co/dfw/dce07b8c-2899/k2-_3d73fbf9-014b-48a8-be67-e7379814f7c1.v4.jpg-369fe01c99718b12839ecbeda57fca9ec0227e8c-webp-450x450.webp'
product_url['35121100']='http://ll-us-i5.wal.co/dfw/dce07b8c-f0c2/k2-_49424e76-16c7-4f8f-89f2-022b43bc6952.v2.jpg-1da2ca6ac434ec50c9cc11e68ef040ac952f2b95-webp-450x450.webp'
product_url['29010048']='http://ll-us-i5.wal.co/dfw/dce07b8c-1074/k2-_2a434f55-7afd-4734-88a2-a2c5fa14b552.v6.jpg-939bce5c7b2746705e6cbad5b189fae8bba9cbc6-webp-450x450.webp'


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
    product_title=str(spell_json['docs'][0]['product_attributes']['product_name']['values'][0]['value'])
# features=["size","wetness indicator","absorb","quality","deliver","ship","offer","softness","weight","price"]
    feature_list=["ship", "price","size","quality","deliver","store","warrant","assembl","remote control","ship to store","store pickup","pickup in store","pick up in store"]
    for feature in features:
        feature_list.extend(feature.split('_'))
    return list(set(feature_list)),product_title

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
    feature_wordcloud_dict={}
    for f in feature_list:
        f=f.lower()
        feature_sent_dict[f]={}
        feature_sent_dict[f]['pos']=0
        feature_sent_dict[f]['neg']=0
        feature_wordcloud_dict[f]=[]
    with open(reviewfile,'r') as review_file:
        for line in review_file:
            review = line.rstrip()
            review_blob = TextBlob(review)
            for sentence in review_blob.sentences:
                try:
                    for feature in feature_sent_dict.keys():
                        if feature in sentence :
                            pol = sentence.sentiment.polarity 
                            if (pol>= 0.70) and (pol <= 0.70) and len(sentence) < 80:
                                feature_wordcloud_dict[feature].append(str(sentence))
                            if pol > 0:
                                feature_sent_dict[feature]['pos']+=1
                            # print sentence
                            if pol < 0:
                                feature_sent_dict[feature]['neg']+=1
                            print sentence
                except ValueError:
                        continue
    df=pd.DataFrame.from_dict(feature_sent_dict, orient='index').reset_index()
    df.cols=['feature','neg','pos']
    df.sort(['pos','neg'],ascending=[False,False],inplace=True)
    df.to_csv(outputfile)
    return feature_sent_dict,feature_wordcloud_dict

def get_feature_senti(productid, get_review_flag=False):
    review_file = './reviews/reviews_{}.txt'.format(productid)
    if get_review_flag:
        get_reviews.get_reviews(product_id)
    wpid=get_wmid(productid)
    wpid=str(wpid.pop())
    feature_list,product_title=get_features(wpid)
    feature_list=modify_features(feature_list)
    outputfile='./reviews/sentiment_%s.txt' %productid
    feature_info,feature_wordcloud_dict=feature_senti(review_file,feature_list,outputfile=outputfile)
    return feature_info,feature_wordcloud_dict,product_title

if __name__=='__main__':
    for product in ['4408441','35121100','29010048']:
        product_id = product
        feature_info,feature_wordcloud_dict,product_title = get_feature_senti(product_id)
        review_summary = {}
        review_summary ["product_id"] = product_id
        review_summary ["product_title"] = product_title
    #     review_summary["url"]="http://ll-us-i5.wal.co/dfw/dce07b8c-57c8/k2-_9398b44d-9567-4beb-841a-53b5c07fd15e.v2.jpg-1a0eb0d389b6f23a8747c7515812d495636fbe53-webp-450x450.webp"
        data = []
        series = [{"name": "Positive", "data": []}, {"name": "Negative", "data": []}]
        categories = []
        feature_wordcloud_dict={k:v for k,v in feature_wordcloud_dict.iteritems() if k in selected_features[product_id]}
        for feat_info in feature_info.iterkeys():
            name = feat_info
            d = feature_info[feat_info]
            pos = d["pos"]
            neg = d["neg"]
            if feat_info in selected_features[product_id]:
                name=name if name not in feature_name_mapping else feature_name_mapping[name]
    #             data_point = {}
    #             data_point["name"] = name 
    #             data_point['y'] = pos + neg
    #             data.append(data_point)
                categories.append(name.title())
                series[0]["data"].append(pos)
                series[1]["data"].append(neg)
    #     review_summary["data"] = data
        review_summary["col_data"] = series
        review_summary["col_cats"] = categories
        demographics = review_demographics.main(product_id)
        for key in ['age_categories', 'age_data', 'ownership_categories', 'ownership_data', 'gender_categories', 'gender_data', 'usage_categories', 'usage_data']:
            review_summary[key] = demographics[key] 
        
        with open("review_data.txt", 'a') as review_data_file:
            review_data_file.write(json.dumps(review_summary) + '\n')
    
        print '########### Word cloud ###################################'
        tags=sentence_clustering.main(feature_wordcloud_dict,5)
        tags_new=[]
        for sentence in tags:
            r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
            size = randint(50,200)
            tags_new.append({'color': (r, g, b), 'tag': sentence, 'size': size})
        cloud_output='./ui/cloud_%s.html'%product_id
        wordcloud.generate_tag_cloud(tags_new,cloud_output)
    #     get_feature_senti('28240450','./reviews/reviews_diapers_28240450.txt')