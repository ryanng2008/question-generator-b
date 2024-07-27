from flask import Flask
from flask_cors import CORS, cross_origin
import algorithm.data_utils as du

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def default():
    return ["This is the production server"]

@app.route("/home")
@cross_origin()
def home():
    return {"players": ["Stephen Curry", "Klay Thompson", "Andre Iguodala", "Draymond Green", "Andrew Bogut"]}

@app.route("/questionlist/<categoryid>", defaults={'count': -1}, methods=['GET'])
@app.route("/questionlist/<categoryid>/<count>")
@cross_origin()
def get_question_list(categoryid: str, count: int):
    return du.questions_from_cid(categoryid, int(count))

@app.route("/categorydetails/<categoryid>", methods=['GET'])
@cross_origin()
def get_category_details(categoryid: str):
    return du.get_category(categoryid)

@app.route("/categorylist", methods=['GET'])
@cross_origin()
def get_all_categories():
    return du.get_all_categories()

if __name__ == "__main__":
    print('server ran')
    app.run(debug=True)
