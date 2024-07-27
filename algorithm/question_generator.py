import random
import re

def question_generator(question_string, rvs, pvs, answer_expressions={}, answer_string='', ):
    evaluated_rvs = get_rvs(rvs)
    variables = get_variables(pvs, evaluated_rvs)
    try:
        question = format(question_string, variables)
        # find a way so that even if there are more variables then you can still run it without errors
    except:
        question = 'Error in question text'
        print('HERE IS THE ERROR \n _________')
        print(question_string)
        #placeholder_indices = [int(idx) for idx in re.findall(r"{(\d+)}(?![{])", question_string)]
        #question = re.sub(r"{\d+}(?![{])", lambda match: variables[placeholder_indices.pop(0)], question_string)

    #answer_variables = get_variables(answer_expressions, variables)
    try:
        #print("answer variables:")
        #print(answer_variables)
        answer = format(answer_string, variables)
    except:
        answer = 'Error in answer text'
        #placeholder_indices = [int(idx) for idx in re.findall(r"{(\d+)}(?![{])", answer_string)]
        #answer = re.sub(r"{\d+}(?![{])", lambda match: answer_variables[placeholder_indices.pop(0)], answer_string)
    #return [question, answer]
    return {'question': question, 'answer': answer}


def get_rvs(rvs):
    values = {}
    for rv in rvs:
        values[rv['name']] = random.randint(int(rv['lb']), int(rv['hb']+1))
    return values

def get_variable_funcs(pvs, evaluated_rvs):
    variables = {}
    for pv_name, eval_string in pvs.items():
        variables[pv_name] = eval_string.format(**evaluated_rvs)
    return variables

def evaluate(func):
    # add some sanitized?
    return eval(func)

def format(question, variables):
    # add some sanitizing?
    return question.format(**variables)

def get_variables(expressions, variables):
    processed_variables = {}
    functions = get_variable_funcs(expressions, variables)
    for name, func in functions.items():
        processed_variables[name] = evaluate(func)
    return processed_variables


if __name__ == "__main__":
    x = question_generator(
        "is {a} or {b} bigger?", 
                    [{'name': 'a','lb': 3, 'hb': 12},
                    {'name': 'b','lb': 3, 'hb': 12},
                    ],
                    {'a': '{a}+6', 'b': '{a} + {b}',},
                    {'answer': '{a}+{b}'},
                    "{answer} dogs"
                    )
    print(x)