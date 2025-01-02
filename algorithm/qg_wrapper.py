import algorithm.question_generator as qg

def generate_question(rvs, pvs, question_string, answer_string=''):
    question = qg.question_generator(rvs, pvs, question_string, answer_string)
    return question

# ---------------

# if __name__ == "__main__":
#     question_object = {
#         'rvs': [
#             {
#             'name': 'a',
#             'lb': 4,
#             'hb': 10},
#             {
#             'name': 'b',
#             'lb': 8,
#             'hb': 18},
#             {
#             'name': 'c',
#             'lb': 2,
#             'hb': 200},
#             ],
#         'pvs': {
#             'BLUERATE': '(a^b) / (b^a)', # maybe you should just use an array to store the extra properties like d.p. (save space)
#             'REDRATE': 'a * c / b'
#         },
#         'question_string': 'If Team Blue makes an average of [[BLUERATE]] passes per game and Team Red makes an average of [[REDRATE]] passes per quarter, which team makes more passes?'
#         }
#     text = generate_question(question_object['rvs'], question_object['pvs'], question_object['question_string'])
#     print(text)