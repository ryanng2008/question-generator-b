import mongo as db
import qg_wrapper as qg
from algorithm import qg_wrapper as new_qg
# Process the mongo data here


# ---------------- PARENT FUNCTIONS ----------------
def get_category(cid: str): # Get Category Object from Category ID
    data = db.get_category_object(cid)
    data['_id'] = str(data['_id'])
    return data

def get_all_categories(): # Get the whole list of category OBJECTS
    datas = db.get_all_categories()
    for data in datas:
        data['_id'] = str(data['_id'])
    return datas

def questions_from_cid(cid: str, count: int):
    qids = get_qids_from_cid(cid)
    questions = []
    if(str(count) == '-1'):
        questions = get_questions_from_qids(qids)
        return questions
    while len(questions) < count:
        if(count < len(questions) + len(qids)):
            new_questions = get_questions_from_qids(qids)
            questions.extend(new_questions[:(count - len(questions))])
            break
        else:
            new_questions = get_questions_from_qids(qids)
            questions.extend(new_questions)
    return questions

def post_new_question(question: str, rvs: list[dict[str, int]], pvs: dict[str, str], answer: str ='No Answer'):
    document = {
        question: question,
        rvs: rvs,
        pvs: pvs,
        answer: answer
    }
    result = db.post_question(document)
    if(result == 0):
        return {'success': False}
    else:
        return {'success': True, 'message': result}


# ---------------- SUB FUNCTIONS ----------------

def get_all_category_ids(): # Get the whole list of category IDs
    cids = db.get_category_id_list()
    return cids

def get_questions_from_qids(qids: list[str]):
    questions = []
    for qid in qids:
        question = get_question_from_qid(qid)
        questions.append(question)
    return questions

def get_qids_from_cid(cid: str): # Get a list of Question IDs from a category
    category = db.get_category_object(cid)
    qids = category['questions']
    return qids



def get_question_from_qid(qid: str): # Generate question from the Question ID 
    # get the question object details from mong
    # input the details into qg_wrapper 
    # return the result
    question_object = db.get_question_object(qid)
    #print('QUESTION OBJECT')
    #print(question_object)
    if question_object == 0:
        return {'question': 'This question does not exist', 'answer': 'No Answer'} # Change this 
    question_string = question_object['question'] or 'question string is not present in the question object'
    rvs = question_object['rvs'] or {}
    pvs = question_object['pvs'] or {}
    answer_string = question_object['answer']
    #print(answer_string)
    # TO DO FIX ANSWER STRING AND ANSWER EXPRESSIONS 

    # MODIFY THIS ORIGIN
    final_question = qg.generate_question(question_string, rvs, pvs, {}, answer_string)

    return final_question

# UNUSED
# ------------------

def get_question_objects(qids: list[str]):
    question_list = db.get_question_objects(qids)
    for question in question_list:
        question['_id'] = str(question['_id'])
    return question_list

#def questions_from_cid(cid: str):
#    qids = get_qids_from_cid(cid)
#    questions = get_questions_from_qids(qids)
#    return questions