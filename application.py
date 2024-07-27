from flask import Flask
import algorithm.data_utils as du

app = Flask(__name__)

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

@app.route("/categorylist")
def get_all_categories():
    return du.get_all_categories()

if __name__ == "__main__":
    print('server ran')
    app.run(debug=False)

    