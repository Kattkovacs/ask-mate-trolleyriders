from datetime import datetime
import connection


def get_list(file, order_by='submission_time', order_direction="asc"):
    questions = connection.csv_to_list_of_dict(file)
    questions = sorting(questions, order_by, order_direction)
    questions = decode_timestamp(questions)
    return questions


def decode_timestamp(comment):
    for item in comment:
        item['submission_time'] = datetime.fromtimestamp(int(item['submission_time']))
    return comment


def filter_by_id(file, question_id, num='id'):
    full_list = connection.csv_to_list_of_dict(file)
    full_list = decode_timestamp(full_list)
    filtered = []
    for item in full_list:
        if item[num] == question_id:
            filtered.append(item)
    return sorting(filtered)


def generate_question(questions, title, message, image=''):
    question = {}
    question['id'] = int(questions[-1]['id']) + 1
    question['submission_time'] = int(round(datetime.timestamp(datetime.now())))
    question['view_number'] = 0
    question['vote_number'] = 0
    question['title'] = title
    question['message'] = message
    question['image'] = image
    question['edit_count'] = 0
    return question


def generate_answer(answers, question_id, message, image=''):
    answer = {}
    answer['id'] = int(answers[-1]['id']) + 1
    answer['submission_time'] = int(round(datetime.timestamp(datetime.now())))
    answer['vote_number'] = 0
    answer['question_id'] = question_id
    answer['message'] = message
    answer['image'] = image
    answer['edit_count'] = 0
    return answer


def sorting(comments, order_by='submission_time', order_direction='asc'):
    if order_direction == 'desc':
        rev = False
    else:
        rev = True
    if order_by == 'view_number' or order_by == 'vote_number':
        return sorted(comments, key=lambda k: int(k[order_by]), reverse=rev)
    else:
        return sorted(comments, key=lambda k: k[order_by], reverse=rev)


def add_question(title, message):
    questions = connection.csv_to_list_of_dict("question.csv")
    new_question = generate_question(questions, title, message)
    questions.append(new_question)
    connection.list_of_dict_to_csv(questions, "question.csv")
    return new_question['id']


def add_answer(question_id, message):
    answers = connection.csv_to_list_of_dict("answer.csv")
    newanswer = generate_answer(answers, question_id, message)
    answers.append(newanswer)
    connection.list_of_dict_to_csv(answers, "answer.csv")


def delete(question_id):
    questions = connection.csv_to_list_of_dict("question.csv")
    for question in questions:
        if question['id'] == question_id:
            questions.remove(question)
    connection.list_of_dict_to_csv(questions, "question.csv")
    answers = connection.csv_to_list_of_dict("answer.csv")
    answers_left = []
    for answer in answers:
        if answer['question_id'] != question_id:
            answers_left.append(answer)
    connection.list_of_dict_to_csv(answers_left, "answer.csv")

