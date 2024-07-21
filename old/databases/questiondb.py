import random

# List of questions will be an object, because it's easier to call using keys + NO NEED TO ITERATE OVER THE WHOLE OBJECT EVER.

# This may seem like waste of space for now, but it stays here until I learn MongoDB. 
questions = {
    "1": [
        'question template {a}', 
        {"a": lambda vars: random.randint(1, 10), "b": lambda vars: random.randint(-1, vars["a"]), "c": lambda vars: random.randint(vars["b"], vars["a"])},
        lambda vars: vars["a"] + vars["b"]],
    "2": [
        'question template 2: {a}',
        {"a": lambda vars: random.randint(1, 20)},
        lambda vars: vars["a"]
    ],
    "3": [
        '$\sqrt{{3}}$',
        {},

    ],
    "4": [
        '$27((3^x)^2 - \\frac{{{a}}}{{{b}}}(3^x)) + 7$ but not rlly enough.',
        {"a": lambda vars: random.randint(1, 100),
        "b": lambda vars: random.randint(1, 100)}
    ],
    "5": [
        'Given that $f\'(x) = xsin^{{{a}}}{{x}}$, find $f(x)$',
        {"a": lambda vars: random.randint(1, 100)}
    ]
}
