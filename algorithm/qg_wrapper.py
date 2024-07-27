import algorithm.question_generator as qg

def generate_question(question_string, rvs, pvs, answer_expressions={}, answer_string='', ):
    question = qg.question_generator(question_string, rvs, pvs, answer_expressions, answer_string)
    return question