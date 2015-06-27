import requests

product_id = "27608624"

url = "http://api.meta-data.glb.prod.walmart.com/reviews/" + product_id + "?page="

num_pages = int(requests.get(url + "1").json().get("payload").get("pagination").get("pages")[-1].get("num"))
review_corpus = []

review_file = '../reviews/reviews_{}.txt'.format(product_id)

with open(review_file, 'w') as review_file:
    for page in range(1, num_pages):
        print "Scanning page {}".format(page)
        page_url = url + str(page)
        reviews = requests.get(page_url).json().get("payload").get("customerReviews")
        for review in reviews:
            review_text = review.get("reviewText")
            review_title = review.get("reviewTitle")
            if review_text is not None:
                review_text = review_text.strip()
            else:
                continue
            if review_title is not None:
                review_title = review_title.strip()
            else:
                continue
            review_text = review_text + review_title
            if len(review_text) > 0:
                review_corpus.append(review_text)
                try:
                    review_file.write(review_text + '\n')
                except:
                    pass