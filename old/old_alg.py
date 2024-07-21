import random
import databases.questiondb as qdb
import databases.categorydb as cdb

def get_question_list(category_id: str): # Wrapper function: Server calls to get a list of questions from category ID
    qid_list = qids_from_category(category_id)
    return list_from_qids(qid_list) # array of arrays w/ question + answer

def qids_from_category(category_id: str): # given the Category ID, gets the respective list of question IDs 
    category = {}
    for item in cdb.categories:
        if 'id' in item and str(item['id']) == category_id:
            category = item
        else:
            print(f'category does not exist: {category_id}') 
    qid_list = category.get('questions', [])
    if qid_list == []:
        print(f'question ID list is empty: {category_id}')
    return qid_list

# ----------- REIMPLEMENT W MONGODB -----------------


def list_from_qids(ids: list[str]): # Wrapper function: Given the list of Question IDs, returns generated questions as strings
    question_list = []
    for id in ids: # For every ID, runs the "question_from_id" function to generate the question then append
        question_object = question_from_id(id)
        if question_object != 0:
            question_list.append(question_object)
    return question_list

# ----------- REIMPLEMENT W MONGODB -----------------

def question_from_id(id: str): # Generates a question given its ID
    question_var = qdb.questions.get(str(id), 0)
    if question_var == 0: return 0 # (DONE) do a check that if it's a None 
    template = question_var[0] if len(question_var) > 0 else ''
    vfunctions = question_var[1] if len(question_var) > 1 else {}
    answer = question_var[2] if len(question_var) > 2 else None
    question_object = question_generator(template, vfunctions, answer)
    return question_object

# ----------- REPLACE WITH NEW -----------------

def question_generator(question_template, variable_functions, answer_function='unknown'): # Underlying funciton to generate the question given the template, variable functions, and answer functions
    if answer_function is None:
        answer_function = 'unknown'
    variables = {}
    for key, func in variable_functions.items():
        variables[key] = func(variables) if callable(func) else func # if it's a function, call it with the parameter of the variables array. If not, Set it equal
    question = question_template.format(**variables) # Substitute variables in the question template using {}
    answer = answer_function(variables) if callable(answer_function) else answer_function
    return [question, answer]

# Example usage
question_template = "If John has {a} apples and Bob has {b} + {c} apples, what is the {{difference}} in their number of apples?"

variable_functions = { # Dictionaries are ordered, so no worries!
    "a": lambda vars: random.randint(1, 10),
    "b": lambda vars: random.randint(-1, vars["a"]), # the input of this lambda should be the variables array.
    "c": lambda vars: random.randint(vars["b"], vars["a"])
}
