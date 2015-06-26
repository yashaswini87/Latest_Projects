from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer


nouns_and_noun_phrases = []
with open("reviews/reviews_ipad.txt") as review_file:
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
            print sentence_features

