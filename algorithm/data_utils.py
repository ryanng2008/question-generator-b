import algorithm.mongo as db
import algorithm.qg_wrapper as qg
from datetime import datetime


# ---------------- PARENT FUNCTIONS ----------------
def post_new_question(question: str, rvs: list[dict[str, int]], pvs: dict[str, str], answer: str='', categoryid: str='', user: str=''):

    document = {
        'question': question,
        'rvs': rvs,
        'pvs': pvs,
        'answer': answer, 
        'createdat': datetime.now().timestamp()
    }
    inserted_id = db.post_question(document)
    # print(user)
    if inserted_id:
        add_category = db.auth_add_q_to_c(inserted_id, categoryid, user)
        if(add_category):
            return {'success': True, 'inserted_id': str(inserted_id)}
        else: 
            return {'success': False, 'message': 'You don\'t have permission to add to this category!'}
    else:
        return {'success': False, 'message': 'Failed to insert question'}
    
def post_new_category(title: str, description: str, tags: list[str], author: str, publiccategory: bool):
    document = {
        'title': title,
        'description': description,
        'tags': tags,
        'author': author,
        'imageLink': '',
        'questions': [],
        'createdat': datetime.now().timestamp()
    }
    if publiccategory:
        document['author'] = 'public'
    inserted_id = db.post_category(document)
    if inserted_id:
        return {'success': True, 'inserted_id': str(inserted_id) }
    return { 'success': False, 'message': 'Failed to post category' }
    
# if __name__ == "__main__":
#     question = ''
#     rvs = [{'name': 'a', 'lb': 1, 'hb': 5}]
#     pvs = [{'varName': 'BALANCE', 'latex': 'a^2'}]
#     answer = ''
#     categoryid = '669cf67d156466a5ee5fe8d3'
#     post_new_question(question, rvs, pvs, answer, categoryid)

def get_category(cid: str): # Get Category Object from Category ID
    data = db.get_category_object(cid)
    #data['_id'] = str(data['_id'])
    return data

def get_categories_by_name(query: str, user: str):
    data = db.search_category_perms(query, user)
    return data

def get_all_categories(): # Get the whole list of category OBJECTS
    datas = db.get_all_categories()
    #for data in datas:
    #    data['_id'] = str(data['_id'])
    return datas

def questions_from_cid(cid: str, count: int):
    qids = get_qids_from_cid(cid)
    questions = []
    if(str(count) == '-1'):
        questions = get_questions_from_qids(qids)
        #print('We are here (v1)')
        #print(questions)
        return questions
    while len(questions) < count:
        if(count < len(questions) + len(qids)):
            new_questions = get_questions_from_qids(qids)
            questions.extend(new_questions[:(count - len(questions))])
            break
        else:
            new_questions = get_questions_from_qids(qids)
            questions.extend(new_questions)
    #print('We are here (v2)')
    #print(questions)
    return questions



# ---------------- SUB FUNCTIONS ----------------

def get_all_category_ids(): # Get the whole list of category IDs
    cids = db.get_category_id_list()
    return cids

def get_questions_from_qids(qids: list[str]):
    # TODO: New Method
    # 1. Bulk Query 
    # 2. Run each object through the generator and generate
    questions = db.get_question_objects(qids)
    # for qid in qids:
    #     question = get_question_from_qid(qid)
    #     questions.append(question)
    question_strings = []
    for question_object in questions:
        question_string = question_object['question'] or 'N/A'
        rvs = question_object['rvs'] or {}
        pvs = question_object['pvs'] or {}
        answer_string = question_object['answer'] or 'N/A'
        final_question = qg.generate_question(rvs, pvs, question_string, answer_string)
        question_strings.append(final_question)
    return question_strings

def get_qids_from_cid(cid: str): # Get a list of Question IDs from a category
    category = db.get_category_object(cid)
    qids = category['questions']
    return qids



def get_question_from_qid(qid: str): # Generate question from the Question ID 
    # get the question object details from mong
    # input the details into qg_wrapper 
    # return the result
    question_object = db.get_question_object(qid)
    if question_object == 0:
        return {'question': 'No Question', 'answer': 'No Answer'} # Change this 
    question_string = question_object['question'] or 'N/A'
    rvs = question_object['rvs'] or {}
    pvs = question_object['pvs'] or {}
    answer_string = question_object['answer'] or 'N/A'
    final_question = qg.generate_question(rvs, pvs, question_string, answer_string)

    return final_question

