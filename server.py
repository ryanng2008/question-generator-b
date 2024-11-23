from flask import Flask, request, jsonify
from flask_cors import CORS
import algorithm.data_utils as du
from config.config import get_config
from bson import json_util

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "https://main.d2ol3fnyw1r498.amplifyapp.com"]}})

@app.route("/home")
def home():
    return {"players": ["Stephen Curry", "Klay Thompson", "Andre Iguodala", "Draymond Green", "Andrew Bogut"]}

@app.route("/questionlist/<categoryid>", defaults={'count': -1})
@app.route("/questionlist/<categoryid>/<count>")
def get_question_list(categoryid: str, count: int):
    content = du.questions_from_cid(categoryid, int(count))
    return json_util.dumps(content)

@app.route("/categorydetails/<categoryid>")
def get_category_details(categoryid: str):
    content = du.get_category(categoryid)
    return json_util.dumps(content)

@app.route("/categorysearch/<namequery>")
def get_category_details_name(namequery: str):
    content = du.get_categories_by_name(namequery)
    return json_util.dumps(content)

@app.route("/categorylist")
def get_all_categories():
    content = du.get_all_categories()
    return json_util.dumps(content)

@app.route("/postquestion", methods=['POST'])
def post_new_question():
    data = request.get_json()
    result = du.post_new_question(data['question'], data['rvs'], data['pvs'], data['answer'], data['categoryid'])
    return jsonify(result)

# @app.before_request
# def before_request():
#     request.start_time = time.time()

# @app.after_request
# def after_request(response):
#     request.end_time = time.time()
#     request_time = request.end_time - request.start_time
#     print(f"Request time: {request_time} seconds")
#     return response

if __name__ == "__main__":
    print('server ran')
    app.run(debug=True)
    app.config.from_object(get_config())

    