from textblob import TextBlob
import json

product_id = '12345678'
review_filename = 'reviews/reviews_ipad.txt'

features = [['screen', 'display'], ['battery'], ['camera']]
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
                    if pol < 0:
                        feat_info["neg"] += 1

review_summary = {"product_id": product_id, "colorByPoint": True}
data = []
for feat_info in feature_info:
    data_point = {}
    data_point["name"] = feat_info["name"].title()
    data_point['y'] = feat_info["pos"] + feat_info["neg"]
    data.append(data_point)

review_summary["data"] = data

with open("review_data.txt", 'w') as review_data_file:
    review_data_file.write(json.dumps(review_summary) + '\n')


