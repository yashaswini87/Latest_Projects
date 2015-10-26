'''
Created on Jun 27, 2015

@author: nsudan1
'''
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import random

def main(feature_dataset_dict,num_clusters=5):
    tags_dict={}
#     filename = './reviews/reviews_%s_%s.txt' % (product_id, cat) 
#     output_filename = './reviews/wordCloud_%s.txt' % product_id 
#     f = open(filename, 'r')
#     out_f = open(output_filename, 'w')
#     feature_dataset_dict = {}
#     for line in f.readlines():
#         line = line.rstrip()
#         review_blob = TextBlob(line)
#         for sentence in review_blob.sentences:
#             for feature in selected_features[product_id]:
#                 sent = str(sentence)
#                 if feature in sent: 
#                     polarity_score = sentence.sentiment.polarity
#                     if (polarity_score >= 0.70) and (polarity_score <= 0.70) and len(sent) < 60:
#                         if feature not in feature_dataset_dict:
#                             feature_dataset_dict[feature] = [sent]
#                         else:
#                             feature_dataset_dict[feature].append(sent)
#     f.close()
    for feature in feature_dataset_dict.iterkeys():
        dataset = feature_dataset_dict[feature]
        if (len(dataset) < num_clusters):
            print 'Representative sentences for feature %s: ' % feature
            for line in dataset:
                line = line.rstrip()
                if line not in tags_dict:
                    tags_dict[line]=1
        else:
            vectorizer = TfidfVectorizer(max_df=0.5, max_features=10000,
                                         stop_words='english')
            X = vectorizer.fit_transform(dataset)
            km = KMeans(n_clusters=num_clusters, init='random', max_iter=100, n_init=1, verbose=1)
            
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
                count = 0
                while (count <= len(indices_with_label)):
                    count = count + 1
                    r = random.randint(0, len(indices_with_label) - 1)
                    randomly_sel_index = indices_with_label[r]
                    rand_line=dataset[randomly_sel_index]
                    if rand_line not in tags_dict:
                        tags_dict[rand_line]=1
                        break
                
                    
#                 out_f.write('%s\n' % dataset[randomly_sel_index])
#     out_f.close()
    return tags_dict.keys()

if __name__=='__main__':
    main(product_id='25059351', cat='TV')
