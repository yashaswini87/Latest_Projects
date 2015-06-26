from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer

pos = 0
neg = 0
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
            if "screen" in sentence or "display" in sentence:
                pol = sentence.sentiment.polarity

                if pol > 0:
                    pos += 1
                    # print sentence
                if pol < 0:
                    neg += 1
                    print sentence


            nouns_and_noun_phrases.append(' '.join(sentence_features["noun_phrases"] + sentence_features["nouns"]))

print "Positive", pos
print "Negative", neg

cv = CountVectorizer(ngram_range=(1,2), min_df=0.01)
cv.fit_transform(nouns_and_noun_phrases)
