from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import algorithm.data_utils as du
from config.config import get_config

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "https://main.d2ol3fnyw1r498.amplifyapp.com"]}})

@app.route("/home")
def home():
    return {"players": ["Stephen Curry", "Klay Thompson", "Andre Iguodala", "Draymond Green", "Andrew Bogut"]}

@app.route("/questionlist/<categoryid>", defaults={'count': -1})
@app.route("/questionlist/<categoryid>/<count>")
def get_question_list(categoryid: str, count: int):
    return du.questions_from_cid(categoryid, int(count))

@app.route("/categorydetails/<categoryid>")
def get_category_details(categoryid: str):
    return du.get_category(categoryid)

@app.route("/categorysearch/<namequery>")
def get_category_details_name(namequery: str):
    return du.get_categories_by_name(namequery)

@app.route("/categorylist")
def get_all_categories():
    return du.get_all_categories()

@app.route("/postquestion", methods=['POST'])
def post_new_question():
    data = request.get_json()
    result = du.post_new_question(data['question'], data['rvs'], data['pvs'], data['answer'], data['categoryid'])
    return jsonify(result)

if __name__ == "__main__":
    print('server ran')
    app.run(debug=False)
    app.config.from_object(get_config())

    