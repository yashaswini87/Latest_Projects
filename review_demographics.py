import requests
import json


def get_chart_data(demographic_data):
    series = []
    categories = []
    category_total = {}

    for key in demographic_data:
        if key is None:
            continue
        categories.append(key)
        count = 0
        for rating in demographic_data[key]:
            count += demographic_data[key][rating]
        category_total[key] = count

    for i in range(1, 6):
        series_element = {"name": i, "data": []}
        for category in categories:
            try:
                series_element["data"].append(round(demographic_data[category][i]*100/float(category_total[category]), 4))
            except:
                series_element["data"].append(0)
        series.append(series_element)

    return json.dumps(categories), json.dumps(series)


def update_dict(data_dict, data_type):
    if data_type not in data_dict:
        data_dict[data_type] = 1
    else:
        data_dict[data_type] += 1

def update_user_data_rating(data_dict, data_type, rating):
    if data_type not in data_dict:
        data_dict[data_type] = {}
    else:
        update_dict(data_dict[data_type], rating)


product_id = "4408441"

url = "http://api.meta-data.glb.prod.walmart.com/reviews/" + product_id + "?page="

num_pages = int(requests.get(url + "1").json().get("payload").get("pagination").get("pages")[-1].get("num"))
review_corpus = []

age = {}
ownership = {}
gender = {}
usage = {}

for page in range(1, num_pages):
    print "Scanning page {}".format(page)
    page_url = url + str(page)
    reviews = requests.get(page_url).json().get("payload").get("customerReviews")
    for review in reviews:
        rating = review.get("rating")
        user_data = review.get("userAttributes")
        update_user_data_rating(age, user_data.get("Age"), rating)
        update_user_data_rating(ownership, user_data.get("Ownership"), rating)
        update_user_data_rating(gender, user_data.get("Gender"), rating)
        update_user_data_rating(usage, user_data.get("Usage"), rating)

print get_chart_data(age)
print get_chart_data(ownership)
print get_chart_data(gender)
print get_chart_data(usage)

