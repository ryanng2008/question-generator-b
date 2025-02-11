import re
import sympy as sp
import random
from latex2sympy2 import latex2sympy
from sympy.parsing.latex import parse_latex




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

def evaluate_pvs(raw_pvs: list[dict[str, str | dict[str, bool | int]]], rvs: dict[str, int]) -> dict[str, float]:
    evaluated_pvs = {}
    try: 
        for item in raw_pvs:
            evaluated_pvs[item['varName']] = evaluate_pv(
                item['latex'], 
                rvs, 
                item.get('coefficient', False), 
                item.get('dp', 0))
    except Exception:
        return {}
    return evaluated_pvs

def evaluate_pv(raw_pv_expression: str, rvs: dict[str, float], coeff: bool = False, dp: int = 0) -> str:
    """
    Evaluate a LaTeX expression with given variable substitutions.

    Returns:
        str: The evaluated result as a string, or None if there's an error.
    """
    # Remove outer braces if present
    #raw_pv_expression = raw_pv_expression.strip("{}")

    try:
        # Convert LaTeX to SymPy expression
        expression = latex2sympy(raw_pv_expression)
    except Exception as e:
        print(f"Error: Failed to parse LaTeX expression. Details: {e}")
        return None

    try:
        # Substitute variables with their values
        substituted = expression.subs(rvs)
    except Exception as e:
        print(f"Error: Failed to substitute variables. Details: {e}")
        return None

    try:
        # Evaluate the expression numerically
        final_value = substituted.evalf()
    except Exception as e:
        print(f"Error: Failed to evaluate expression. Details: {e}")
        return None

    # Ensure the result is a SymPy Float
    if not isinstance(final_value, sp.Float):
        print("Error: Result is not a numerical value.")
        return None

    # Truncate the result to the specified number of decimal places
    rounded_val = truncate(final_value, dp)

    # Handle coefficients if required
    if coeff:
        if rounded_val == 1:
            return ""
        if rounded_val == -1:
            return "-"

    return str(rounded_val)


def evaluate_pv_old(raw_pv_expression: str, rvs: dict[str, float], coeff: bool=False, dp: int=0) -> str: # float | int
    # STUFF TO ADD
    # Function filters
    raw_pv_expression = raw_pv_expression.strip("{}") # why?
    # print(raw_pv_expression)
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
    
    # return as str here
    final_value = substituted.evalf()
    #print(f'final value: {final_value}')
    if not isinstance(final_value, sp.Float):
        print('Error: not an instance of Float')
        # equivalent to syntax error
        return None
    rounded_val = truncate(final_value, dp)
    if coeff:
        if rounded_val == 1:
            return ''
        if rounded_val == -1:
            return '-'
    return str(rounded_val)
    
    #raw pv expression is a string, rvs is a hashmap (str, float)
    # convert raw_pv into sympy expression
    # substitute it in
    # return a value

def truncate(number: int | float, dp: int = 0) -> int | float:
    if dp == 0:
        return int(number)
    multiplier = 10 ** dp
    return int(number * multiplier) / multiplier

# QUESTION STRING SUBSTITUTION (plus answer string)
# - input: string with "[[variable]]" delimiting + pvs dict (name, value)
# - custom substitution function to replace with the hashmap values

def substitute(pvs: dict[str, str], question_string: str) -> str:
    # implement exceptions later
    subbed_string = question_string
    for key, value in pvs.items():
        #print(f'{key} and {value}')
        if value is None:
            print(f'Error: Value is none for pair {key} and {value}')
            continue 
        # Replace [[key]] in the string with its corresponding value
        # subbed_string = subbed_string.replace(f"[[{key}]]", value)
        subbed_string = re.sub(rf"\[\[{key}\]\]", value, subbed_string, flags=re.IGNORECASE)

    # print(f'subbed question string: {subbed_string}')
    return subbed_string


## PARENT FUNCTION - does all of it
def question_generator(raw_rvs, raw_pvs, question_string, answer_string='') -> str:
    evaluated_rvs = evaluate_rvs(raw_rvs)
    evaluated_pvs = evaluate_pvs(raw_pvs, evaluated_rvs)
    final_question = substitute(evaluated_pvs, question_string)
    #print(f'FINAL QUESTION, {final_question}')
    final_answer = substitute(evaluated_pvs, answer_string)
    return { 'question': final_question, 'answer': final_answer}

# print(evaluate_pv2('\\frac{3}{5}', {}, False, 1))



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