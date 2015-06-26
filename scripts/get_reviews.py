import requests

product_id = "28240450"

url = "http://api.meta-data.glb.prod.walmart.com/reviews/" + product_id + "?page="

num_pages = int(requests.get(url + "1").json().get("payload").get("pagination").get("pages")[-1].get("num"))
review_corpus = []

with open('../reviews/reviews_diapers_28240450.txt', 'w') as review_file:
    for page in range(1, num_pages):
        page_url = url + str(page)
        reviews = requests.get(page_url).json().get("payload").get("customerReviews")
        for review in reviews:
            review_text = review.get("reviewText").strip()
            if len(review_text) > 0:
                review_corpus.append(review_text)
                try:
                    review_file.write(review_text + '\n')
                except:
                    pass