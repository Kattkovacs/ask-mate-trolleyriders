from datetime import datetime
import connection


def get_list(file, order_by='submission_time', order_direction="asc"):
    questions = connection.csv_to_list_of_dict(file)
    questions = sorting(questions, order_by, order_direction)
    questions = decode_timestamp(questions)
    return questions


def decode_timestamp(list):
    for item in list:
        item['submission_time'] = datetime.fromtimestamp(int(item['submission_time']))
    return list


def filter_by_id(file, question_id, id='id'):
    questions = connection.csv_to_list_of_dict(file)
    questions = decode_timestamp(questions)
    filtered = []
    for item in questions:
        if item[id] == question_id:
            filtered.append(item)
    return sorting(filtered)


def generate_question(leng, title, message, image=''):
    question = {}
    question['id'] = leng + 1
    question['submission_time'] = int(round(datetime.timestamp(datetime.now())))
    question['view_number'] = 0
    question['vote_number'] = 0
    question['title'] = title
    question['message'] = message
    question['image'] = image
    return question


def generate_answer(leng, question_id, message, image=''):
    answer = {}
    answer['id'] = leng + 1
    answer['submission_time'] = int(round(datetime.timestamp(datetime.now())))
    answer['vote_number'] = 0
    answer['question_id'] = question_id
    answer['message'] = message
    answer['image'] = image
    return answer


def sorting(list, order_by='submission_time', order_direction='asc'):
    if order_direction == 'desc':
        dir = False
    else:
        dir = True
    if order_by == 'view_number' or order_by == 'vote_number':
        return sorted(list, key=lambda k: int(k[order_by]), reverse=dir)
    else:
        return sorted(list, key=lambda k: k[order_by], reverse=dir)


def add_question(title, message):
    questions = connection.csv_to_list_of_dict("question.csv")
    new_question = generate_question(len(questions), title, message)
    questions.append(new_question)
    connection.list_of_dict_to_csv(questions, "question.csv")
    return new_question['id']

def add_answer(question_id, message):
    answers = connection.csv_to_list_of_dict("answer.csv")
    newanswer = generate_answer(len(answers), question_id, message)
    answers.append(newanswer)
    connection.list_of_dict_to_csv(answers, "answer.csv")

