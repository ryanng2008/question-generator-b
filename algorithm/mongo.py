#import pymongo
from pymongo.mongo_client import MongoClient
#from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from bson import json_util

uri = 'mongodb+srv://ryandoesnothing1:0wt60G4Vv2e3fv0u@firstvisionary.06rzakp.mongodb.net/'
db_name = 'main'
category_collection = 'categories'
questions_collection = 'questions'
client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True) # Fix this temporary thing
db = client[db_name]
categories = db[category_collection]
questions = db[questions_collection]

# TO DO: Wrap everything in a try catch

def post_question(question_object: dict):
    try:
        result = questions.insert_one(question_object)
        return result.inserted_id
    except Exception as e:
        print("Error inserting question document: ", e)
        return None


# WORKING - # Get Full Category ID List
def get_category_id_list():
    category_ids = categories.find({}, {'_id': True})
    category_id_list = []
    for document in category_ids:
        category_id_list.append(document['_id'])
    print(category_id_list)
    return category_id_list

# WORKING - Get All Category Objects (Raw)

def get_all_categories():
    category_objects = []
    categories_get = categories.find({})
    category_objects = list(categories_get)
    for item in category_objects:
        item["_id"] = str(item["_id"])
    #print(category_objects)
    return category_objects

# WORKING - Get Category Object from Category ID
def get_category_object(category_id):
    cat_object = categories.find_one({'_id': ObjectId(str(category_id))}) # THIS IS THE QUERY
    if cat_object == None:
        return 0
    cat_object['_id'] = str(cat_object['_id'])
    print(cat_object)
    return cat_object

def get_category_name_regex(query: str):
    results = categories.find({"title": {"$regex": query, "$options": "i"}})
    categories_list = list(results)
    for item in categories_list:
        item['_id'] = str(item['_id'])
    return categories_list

def search_category_perms(query: str, user: str):
    # TODO: ADD PERMS LOGIC WITH USER 
    results = categories.find({"name": {"$regex": query, "$options": "i"}})
    categories_list = results.to_list()
    return categories_list

# WORKING - Get Question Objects from Question ID
def get_question_object(question_id):
    #print(f'getting {question_id}')
    #question_object = questions.find_one({'questionId': str(question_id)})
    question_object = questions.find_one({'_id': ObjectId(str(question_id))}) # THIS IS THE QUERY 
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
    question_objects = []
    for question_id in question_ids:
        question_object = get_question_object(question_id)
        if question_object != 0: 
            question_objects.append(question_object)
    print(question_objects)
    return question_objects

def add_question_to_category(qid, cid):
    try:
        answer = categories.update_one({"_id": ObjectId(cid)}, {"$push": {"questions": qid}})
        return answer.matched_count > 0
    except Exception as e:
        print(f'Error adding question {qid} to category {cid}')
        return None