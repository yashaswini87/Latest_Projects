import requests

product_id = "33093101"

url = "http://api.meta-data.glb.prod.walmart.com/reviews/" + product_id + "?page="

num_pages = int(requests.get(url + "1").json().get("payload").get("pagination").get("pages")[-1].get("num"))
review_corpus = []

with open('reviews.txt', 'w') as review_file:
    for page in range(1, num_pages):
        page_url = url + str(page)
        reviews = requests.get(page_url).json().get("payload").get("customerReviews")
        for review in reviews:
            review_corpus.append(review.get("reviewText"))
            try:
                review_file.write(review.get("reviewText") + '\n')
            except:
                pass