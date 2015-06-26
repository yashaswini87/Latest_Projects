from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer

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

with open("reviews/reviews_ipad.txt") as review_file:
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

print feature_info


