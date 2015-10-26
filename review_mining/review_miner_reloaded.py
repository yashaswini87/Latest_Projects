from textblob import TextBlob
import json
from wordcloud import generate_tag_cloud
from random import randint


product_id = '27608624'
review_filename = 'reviews/reviews_{}.txt'.format(product_id)
informative_sentences = []

features = [['screen', 'display'], ['battery'], ['camera'], ["shipping"], ["price"]]
features = [['screen', 'display'], ['battery'], ['camera'], ["video"], ["reception"], ["shipping"], ["price"]]
sentiment = []

feature_info = []
for feature in features:
    feat_info = {}
    feat_info['name'] = feature[0]
    if len(feature) > 0:
        feat_info['synonyms'] = feature
    feat_info['pos'] = 0
    feat_info['neg'] = 0
    feature_info.append(feat_info)

with open(review_filename) as review_file:
    for line in review_file:
        review = line.strip()
        review_blob = TextBlob(review)
        for sentence in review_blob.sentences:
            sentence_features = {}
            sentence_features["sentence"] = sentence
            sentence_features["polarity"] = sentence.sentiment.polarity

            for feat_info in feature_info:
                if any(feat in sentence for feat in feat_info['synonyms']):
                    pol = sentence.sentiment.polarity

                    if pol > 0:
                        feat_info["pos"] += 1
                        if pol == 1.0 and len(sentence) < 40:
                            informative_sentences.append((str(sentence), pol))
                            print pol
                    if pol < 0:
                        feat_info["neg"] += 1
                        if pol == -1.0 and len(sentence) < 40:
                            informative_sentences.append((str(sentence), -1*pol))

review_summary = {"product_id": product_id}
data = []
series = [{"name": "Positive", "data": []}, {"name": "Negative", "data": []}]
categories = []

for feat_info in feature_info:
    data_point = {}
    data_point["name"] = feat_info["name"].title()
    data_point['y'] = feat_info["pos"] + feat_info["neg"]
    data.append(data_point)
    categories.append(feat_info["name"].title())
    series[0]["data"].append(feat_info["pos"])
    series[1]["data"].append(feat_info["neg"])

review_summary["data"] = data
review_summary["col_data"] = series
review_summary["col_cats"] = categories

with open("review_data.txt", 'a') as review_data_file:
    review_data_file.write(json.dumps(review_summary) + '\n')


tags = []
#3498db

for sentence in informative_sentences:
    r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
    size = int(100 * sentence[1])
    tags.append({'color': (r, g, b), 'tag': sentence[0], 'size': size})

generate_tag_cloud(tags)