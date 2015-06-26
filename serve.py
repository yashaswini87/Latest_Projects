from flask import Flask
import json
from flask import request

app = Flask(__name__)

@app.route("/")
def get_stats():
    product_id = request.args.get('productId')
    review_data = {
            "Product Id": product_id,
            "colorByPoint": True,
            "data": [{
                "name": "Speed",
                "y": 56.33
            }, {
                "name": "Screen",
                "y": 24.035,
                "sliced": True,
                "selected": True
            }, {
                "name": "Resolution",
                "y": 10.38
            }, {
                "name": "Shipping",
                "y": 4.77
            }, {
                "name": "Assembly",
                "y": 0.91
            }, {
                "name": "Battery",
                "y": 0.2
            }]
        }
    return json.dumps(review_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)
