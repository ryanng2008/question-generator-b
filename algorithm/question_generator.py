import sympy as sp
import random


# RV EVALUATION
# - Initial input: array of hashmaps w/ pairs (variable, str) (lb, int) (hb, int)
# for each, generate random integer (max inclusive); return new hashmap

def evaluate_rvs(raw_rvs: list[dict[str, int]]) -> dict[str, int]:
    evaluated_rvs: dict[str, int] = {}
    for rv in raw_rvs:
        value = random.randint(int(rv['lb']), int(rv['hb']))
        evaluated_rvs[rv['name']] = value
    return evaluated_rvs
    

# PV EVALUATION

# - Initial input: hashmap (variable, clean_expression)
# - parse each expression with sympy, return a new hashmap

def evaluate_pvs(raw_pvs: list[dict[str, str]], rvs: dict[str, int]) -> dict[str, float]:
    evaluated_pvs = {}
    try: 
        for item in raw_pvs:
            evaluated_pvs[item['varName']] = evaluate_pv(item['latex'], rvs)
    except Exception as e:
        return {}
    return evaluated_pvs
def evaluate_pv(raw_pv_expression: str, rvs: dict[str, float]) -> float:
    # STUFF TO ADD
    # Function filters
    print(raw_pv_expression)
    raw_pv_expression = raw_pv_expression.strip("{}")
    print(raw_pv_expression)
    try:
        expression = sp.sympify(raw_pv_expression)
        #print(f'expression: {expression} of type {type(expression)}')
    except:
        # syntax error
        print('Error: syntax error while running sympify')
        return None
    rvs_as_tuples = list(rvs.items())
    try: 
        substituted = expression.subs(rvs_as_tuples)
        #print(f'substituted: {substituted}')
    except:
        print('Error: syntax error while running subs')
        return None

    final_value = substituted.evalf()
    #print(f'final value: {final_value}')
    if not isinstance(final_value, sp.Float):
        print('Error: not an instance of Float')
        # equivalent to syntax error
        return None
    return float(final_value)
    #raw pv expression is a string, rvs is a hashmap (str, float)
    # convert raw_pv into sympy expression
    # substitute it in
    # return a value



# QUESTION STRING SUBSTITUTION (plus answer string)
# - input: string with "[[variable]]" delimiting + pvs dict (name, value)
# - custom substitution function to replace with the hashmap values

def substitute(pvs: dict[str, float], question_string: str) -> str:
    # implement exceptions later
    subbed_string = question_string
    for key, value in pvs.items():
        #print(f'{key} and {value}')
        if value is None:
            print(f'Error: Value is none for pair {key} and {value}')
            continue 
        # Replace [[key]] in the string with its corresponding value
        subbed_string = subbed_string.replace(f"[[{key}]]", str(round(value, 2)))
    print(f'subbed question string: {subbed_string}')
    return subbed_string


## PARENT FUNCTION - does all of it
def question_generator(raw_rvs, raw_pvs, question_string, answer_string='') -> str:
    evaluated_rvs = evaluate_rvs(raw_rvs)
    evaluated_pvs = evaluate_pvs(raw_pvs, evaluated_rvs)
    final_question = substitute(evaluated_pvs, question_string)
    #print(f'FINAL QUESTION, {final_question}')
    final_answer = ''#substitute_question(evaluated_pvs, answer_string)
    return { 'question': final_question, 'answer': final_answer}




# PLANNING & SYMPY TESTING


# x, y, z = symbols("x y z")

# expr = cos(x) + 1
# expr.subs(x, y)


# str_expr = "tan sin 434fh"
# expr = sympify(str_expr)
# value = expr.subs('EN', 2)
# print(value)

# rvs_dict = {
#     'A': 3,
#     'B': 4,
#     'C': 5
# }
# subs_values = list(rvs_dict.items())


# PRIMITIVE FUNCTIONS: 
# - given the question string, rvs, pvs, and answer string, 
# - evaluate rvs into values
# - evaluate pvs into values (input rvs & pvs) - NEEDS SYMPY
# - substitute into question string 