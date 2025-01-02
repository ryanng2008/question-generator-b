#import pymongo
from pymongo.mongo_client import MongoClient
#from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from bson import json_util
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv('URI')
db_name = os.getenv('DB_NAME')
category_collection = os.getenv('CATEGORY_COLL')
questions_collection = os.getenv('QUESTIONS_COLL')
users_collection = os.getenv('USERS_COLL')
client = MongoClient(uri, tls=True) # Fix this temporary thing
db = client[db_name]
categories = db[category_collection]
questions = db[questions_collection]
users = db[users_collection]

# PENDING TESTING - no reason it shouldn't work
def post_user(user_object: dict):
    try:
        result = users.insert_one(user_object)
        return result.inserted_id
    except Exception as e:
        # print("Error registering user: ", e)
        return None

# PENDING TESTING - no reason it shouldn't work
def fetch_user(username: str):
    try: 
        user_object = users.find_one({'username': username})
    except Exception as e:
        # print(f'Error fetching user {username}', e)
        return 0
    if user_object == None:
        return 0
    user_object['_id'] = str(user_object['_id'])
    # print(user_object)
    return user_object


# WORKING - Post question 
def post_question(question_object: dict):
    try:
        result = questions.insert_one(question_object)
        return result.inserted_id
    except Exception as e:
        # print("Error inserting question document: ", e)
        return None
    
def post_category(category_object: dict):
    try: 
        result = categories.insert_one(category_object)
        return result.inserted_id
    except Exception as e:
        # print("Error inserting question document: ", e)
        return None

# WORKING - # Get Full Category ID List
def get_category_id_list():
    category_id_list = []
    try: 
        category_ids = categories.find({}, {'_id': True})
    except Exception as e:
        print("Error getting category ID list: ", e)
        return category_id_list
    for document in category_ids:
        category_id_list.append(document['_id'])
    print(category_id_list)
    return category_id_list

# WORKING - Get All Category Objects (Raw)

def get_all_categories():
    category_objects = []
    try:
        categories_get = categories.find({})
    except Exception as e:
        # print("Error getting all category objects: ", e)
        return category_objects
    category_objects = list(categories_get)
    for item in category_objects:
        item["_id"] = str(item["_id"])
    #print(category_objects)
    return category_objects

# WORKING - Get Category Object from Category ID
def get_category_object(category_id):
    try: 
        cat_object = categories.find_one({'_id': ObjectId(str(category_id))}) # THIS IS THE QUERY
    except Exception as e: 
        print(f"Error getting category object from ID {category_id}", e)
        return 0
    if cat_object == None:
        return 0
    cat_object['_id'] = str(cat_object['_id'])
    print(cat_object)
    return cat_object

def search_category_perms(query: str, user: str):
    try: 
        results = categories.find({"title": {"$regex": query, "$options": "i"}})
    except Exception as e:
        print(f"Error querying categories with '{query}' for user {user}", e)
        return []
    categories_list = list(results)
    if categories_list is None:
        return 'FUCK ME'
    for item in categories_list:
        item['_id'] = str(item['_id'])
    return categories_list

def get_category_regex(query: str):

    # TODO: ADD PERMS LOGIC WITH USER 
    return

# WORKING - Get Question Objects from Question ID
def get_question_object(question_id):
    #print(f'getting {question_id}')
    #question_object = questions.find_one({'questionId': str(question_id)})
    try: 
        question_object = questions.find_one({'_id': ObjectId(str(question_id))}) # THIS IS THE QUERY
    except Exception as e:
        print(f'Error getting question object for {question_id}', e)
        return 0 
    # When you do find, you need to do for document in cursor.
    #print(question_object)
    if question_object is None:
        print(f'FAILED: Object for QID ({question_id}) does not exist. (above)')
        return 0
    #print(question_object)
    return question_object

# Array Get version of this
# TODO: Make this a bulk query
def get_question_objects(question_ids):
    objectid_array = [ObjectId(id_str) for id_str in question_ids]
    try:
        question_objects = questions.find({"_id": {"$in": objectid_array}})
    except Exception as e:
        print('Error getting question objects from ID array', e)
        return []
    return list(question_objects)

def add_question_to_category(qid, cid):
    try:
        answer = categories.update_one(
            {"_id": ObjectId(cid)}, 
            {"$push": {"questions": str(qid)}}) # or str(qid) if there are errors
        return answer.matched_count > 0
    except Exception as e:
        print(f'Error adding question {qid} to category {cid}: {e}')
        return None
    
def auth_add_q_to_c(qid, cid, user):
    try:
        answer = categories.update_one(
            {"_id": ObjectId(cid), "author": user}, 
            {"$push": {"questions": str(qid)}}) # or str(qid) if there are errors
        return answer.matched_count > 0
    except Exception as e:
        print(f'Error adding question {qid} to category {cid}: {e}')
        return None