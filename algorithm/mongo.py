# RAW DATA EXTRACTION FROM MONGO
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId


uri = 'mongodb+srv://ryandoesnothing1:0wt60G4Vv2e3fv0u@firstvisionary.06rzakp.mongodb.net/?retryWrites=true&w=majority&appName=FirstVisionary'
db_name = 'main'
category_collection = 'categories'
questions_collection = 'questions'
client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
db = client[db_name]
categories = db[category_collection]
questions = db[questions_collection]

# WORKING - # Get Full Category ID List
def get_category_id_list():
    category_ids = categories.find({}, {'id': True})
    category_id_list = []
    for document in category_ids:
        category_id_list.append(document['id'])
    print(category_id_list)
    return category_id_list

# WORKING - Get All Category Objects (Raw)

def get_all_categories():
    category_objects = []
    categories_get = categories.find({})
    for document in categories_get:
        category_objects.append(document)
    #print(category_objects)
    return category_objects

# WORKING - Get Category Object from Category ID
def get_category_object(category_id):
    cat_object = categories.find_one({'_id': ObjectId(str(category_id))}) # THIS IS THE QUERY
    if cat_object is None:
        return 0
    print(cat_object)
    return cat_object

# WORKING - Get Question Objects from Question ID
def get_question_object(question_id):
    print(f'getting {question_id}')
    #question_object = questions.find_one({'questionId': str(question_id)})
    question_object = questions.find_one({'_id': ObjectId(str(question_id))}) # THIS IS THE QUERY 
    # When you do find, you need to do for document in cursor.
    print(question_object)
    if question_object is None:
        print(f'FAILED: Object for QID ({question_id}) does not exist. (above)')
        return 0
    #print(question_object)
    return question_object

# Array Get version of this
def get_question_objects(question_ids):
    question_objects = []
    for question_id in question_ids:
        question_object = get_question_object(question_id)
        if question_object != 0: 
            question_objects.append(question_object)
    print(question_objects)
    return question_objects

# SANDBOXING

if __name__ == "__main__":
    question_object = questions.find({"_id": ObjectId('669cf67d156466a5ee5fe8d1')})
    for document in question_object:
        print('yo')
        print(document)
    print(question_object)


#get_question_object(2)