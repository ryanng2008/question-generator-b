from functools import wraps
import os
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import algorithm.data_utils as du
import algorithm.auth_utils as au
import algorithm.encryption as enc
from config.config import get_config
from bson import json_util

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": [
    os.getenv('LOCALHOST'), 
    os.getenv('PRODUCTION_AWS'), 
    os.getenv('PRODUCTION_RENDER')
    ]}})

def token_required_cookies(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("Cookies in request:", request.headers.get('Cookie'))  # Log raw Cookie header
        print("Parsed cookies:", request.cookies)
        token = request.cookies.get('token', 0)  # Get the token from cookies
        print(token)
        if token == 0:
            # Questionable about this return
            return jsonify({'message': 'Token is missing!'}), 401
        result = enc.validate_token(token)
        if not result['success']:
            # Questionable about this return also
            return jsonify({'message': result['message']}), 401
        # U need to figure out what you want to return here. The user? Other details?
        identity = result['identity']
        return f(identity, *args, **kwargs)
    return decorated

# ATM this returns the user string
def token_required(f): 
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
            print(token)
        # if 'x-access-token' in request.headers:
        #     token = request.headers['x-access-token']
        if not token: # this should be right  yeah it is because of 0
            print('missing')
            return jsonify({'message': 'Token is missing!'})
        result = enc.validate_token(token)
        if not result['success']:
            print('failed token')
            # Questionable about this return also
            return jsonify({'message': result['message']})
        # U need to figure out what you want to return here. The user? Other details?
        identity = result['identity']
        # print(identity)
        return f(identity, *args, **kwargs)
        # try:
        #     # Replace with your own logic - check the shit
        #     data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        #     current_user = data['public_id']  # Get user ID from token
        # except:
        #     return jsonify({'message': 'Token is invalid!'}), 403
        # identity = ''
        # return f(identity, *args, **kwargs)

    return decorated

def user_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = None
        if 'X-Username' in request.headers:
            user = request.headers['X-Username']
            print(user)
        if not user: 
            print('missing')
            return jsonify({'message': 'User is missing!'}), 401
        return f(user, *args, **kwargs)
    return decorated

@app.route("/home")
def home():
    cookie = request.headers.get('Cookie')
    token = request.cookies.get('token')
    print('Cookie: ')
    print(cookie)
    print('Token: ')
    print(token)
    return {"cookie": cookie, "token": token, "players": ["Stephen Curry", "Klay Thompson", "Andre Iguodala", "Draymond Green", "Andrew Bogut"]}

@app.route("/questionlist/<categoryid>", defaults={'count': -1})
@app.route("/questionlist/<categoryid>/<count>")
def get_question_list(categoryid: str, count: int):
    content = du.questions_from_cid(categoryid, int(count))
    print(content)
    return json_util.dumps(content)

@app.route("/categorydetails/<categoryid>")
def get_category_details(categoryid: str):
    content = du.get_category(categoryid)
    return json_util.dumps(content)

@app.route("/categorysearch/<namequery>", defaults={'user': ''})
@app.route("/categorysearch/<namequery>/<user>")
def get_category_details_name(namequery: str, user: str):
    content = du.get_categories_by_name(namequery, user)
    return json_util.dumps(content)

@app.route("/categorylist")
def get_all_categories():
    content = du.get_all_categories()
    return json_util.dumps(content)


@app.route("/postquestion", methods=['POST'])
@token_required
def post_new_question(user):
    data = request.get_json()
    # implement the user (+ jwt) here in parameters
    result = du.post_new_question(data['question'], data['rvs'], data['pvs'], data['answer'], data['categoryid'], user)
    return jsonify(result)


@app.route("/postcategory", methods=['POST'])
@token_required
def post_new_category(user):
    data = request.get_json()
    print(data)
    print(user)
    result = du.post_new_category(data['title'], data['description'], data['tags'], user)
    return jsonify(result)

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    login = au.handle_login(username, password)
    if login['success']:
        response = make_response(jsonify({ 
            'success': login['success'], 
            'message': login['message'], 
            'token': login['token'] })
            , 200)
        # response.set_cookie(
        #     "token",
        #     value=login['token'],
        #     expires=login['expires'],
        #     max_age=login['max_age'],
        #     httponly=True,    # Prevent JavaScript access
        #     secure=False,      # TRUE: Only over HTTPS in production
        #     samesite="Lax" # STRICT: Protect against CSRF
        # )
        return response, 200
    return jsonify(login), 401

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    register = au.handle_register(username, password)
    if(register['success']):
        response = make_response(jsonify({ 'success': register['success'], 'message': register['message'] }), 200)
        # response.set_cookie(
        #     "token",
        #     value=register['token'],
        #     expires=register['expires'],
        #     max_age=register['max_age'],
        #     httponly=True,    # Prevent JavaScript access
        #     secure=False,      # Only over HTTPS in production
        #     samesite="Strict" # Protect against CSRF
        # )
        return response, 200
    return register

@app.route("/user", methods=['GET'])
@token_required
def get_user(user_identity): # the token required function returns the function where the first param is identity
    if not user_identity:
        return jsonify({'error': 'User not found!'}), 404
    # print(user_identity)
    return jsonify({ "identity": user_identity })

if __name__ == "__main__":
    print('server ran')
    app.run(debug=True)
    app.config.from_object(get_config())



# @app.before_request
# def before_request():
#     request.start_time = time.time()

# @app.after_request
# def after_request(response):
#     request.end_time = time.time()
#     request_time = request.end_time - request.start_time
#     print(f"Request time: {request_time} seconds")
#     return response
