from flask import Flask
import json
from flask import request
from flask import Response

app = Flask(__name__)

review_summaries = {}
def load_summaries():
    with open('review_data.txt') as summary_file:
        for line in summary_file:
            rev_summary = json.loads(line.strip())
            review_summaries[rev_summary["product_id"]] = rev_summary


@app.route("/")
def get_review_data():
    product_id = request.args.get('productId')
    if product_id in review_summaries:
        data = review_summaries[product_id]
    else:
        data = {}
    resp = Response(json.dumps(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = "GET, POST, PUT, OPTIONS"
    resp.headers['Access-Control-Allow-Headers'] = "Content-Type"
    return resp

@app.route("/dashboard")
def get_dashboard():
    with open('ui/dashboard-dynamic.html') as dashboard:
        return dashboard.read()


if __name__ == "__main__":
    load_summaries()
    app.run(host='0.0.0.0', port=8888)
