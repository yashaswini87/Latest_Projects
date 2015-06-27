'''
Created on Jun 27, 2015

@author: nsudan1
'''
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from time import time
import random
from textblob import TextBlob

selected_features = {}
selected_features['35121100'] = ['height', 'weight', 'length', 'color', 'fabric', 'instructions', 'brand', 'assemble', 'price','ship','deliver', 'warranty']
selected_features['34390987'] = ['height', 'weight', 'brand', 'assemble', 'price', 'ship', 'warranty']
selected_features['25059351'] = ['price','quality','screen','brand','remote','control','rate','weight','resolution','warranty','ship','deliver']
selected_features['4408441'] = ['quality','finish','price','ship','wood','deliver','store','size','material','color', 'warranty']

def main(product_id, cat):
    filename = './reviews/reviews_%s_%s.txt' % (product_id, cat) 
    f = open(filename, 'r')
    feature_dataset_dict = {}
    for line in f.readlines():
        line = line.rstrip()
        review_blob = TextBlob(line)
        for sentence in review_blob.sentences:
            for feature in selected_features[product_id]:
                sent = str(sentence)
                if feature in sent: 
                    polarity_score = sentence.sentiment.polarity
                    if (polarity_score >= 0.70) and (polarity_score <= 0.70) and len(sent) < 60:
                        if feature not in feature_dataset_dict:
                            feature_dataset_dict[feature] = [sent]
                        else:
                            feature_dataset_dict[feature].append(sent)
    
    for feature in feature_dataset_dict.iterkeys():
        dataset = feature_dataset_dict[feature]
        if (len(dataset) < 3):
            print '****************************************'
            print 'Representative sentences for feature %s: ' % feature
            for line in dataset:
                line = line.rstrip()
                print line
        else:
            t0 = time()
            vectorizer = TfidfVectorizer(max_df=0.5, max_features=10000,
                                         stop_words='english')
            X = vectorizer.fit_transform(dataset)
            km = KMeans(n_clusters=3, init='random', max_iter=100, n_init=1, verbose=1)
            
            t0 = time()
            km.fit(X)
            label_dict = {}
            i = 0
            for label in km.labels_:
                if label not in label_dict:
                    label_dict[label] = [i]
                else:
                    label_dict[label].append(i) 
                i = i + 1
            print '****************************************'
            print 'Representative sentences for feature %s: ' % feature
            for label in label_dict.iterkeys():
                indices_with_label = label_dict[label]
                r = random.randint(0, len(indices_with_label) - 1)
                randomly_sel_index = indices_with_label[r]
                print dataset[randomly_sel_index]
    
if __name__=='__main__':
    main(product_id='25059351', cat='TV')
