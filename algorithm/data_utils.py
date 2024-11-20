import algorithm.mongo as db
import algorithm.qg_wrapper as qg

# ---------------- PARENT FUNCTIONS ----------------
def post_new_question(question: str, rvs: list[dict[str, int]], pvs: dict[str, str], answer: str='', categoryid: str=''):
    document = {
        'question': question,
        'rvs': rvs,
        'pvs': pvs,
        'answer': answer, 
    }
    inserted_id = db.post_question(document)
    if inserted_id:
        add_category = db.add_question_to_category(categoryid, inserted_id)
        if(add_category):
            return {'success': True, 'inserted_id': str(inserted_id)}
    else:
        return {'success': False, 'message': 'Failed to insert question'}
    
def get_category(cid: str): # Get Category Object from Category ID
    data = db.get_category_object(cid)
    #data['_id'] = str(data['_id'])
    return data

def get_categories_by_name(query: str):
    data = db.get_category_name_regex(query)
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
    answer_string = question_object['answer'] or 'answer string is not present in the answer object'
    #print(answer_string)
    # TODO: FIX ANSWER STRING AND ANSWER EXPRESSIONS 

    # MODIFY THIS ORIGIN
    final_question = qg.generate_question(rvs, pvs, question_string, answer_string)

    return final_question

