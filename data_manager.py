from datetime import datetime
import connection
from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor


# def get_list(file, order_by='submission_time', order_direction="asc"):
#     questions = connection.csv_to_list_of_dict(file)
#     questions = sorting(questions, order_by, order_direction)
#     questions = decode_timestamp(questions)
#     return questions

@connection.connection_handler
def get_list(cursor: RealDictCursor, order_by, order_direction) -> list:
    if order_direction == 'ASC':
        query = sql.SQL("SELECT * FROM question ORDER BY {o} ASC").format(o=sql.Identifier(order_by))
        cursor.execute(query)
    else:
        query = sql.SQL("SELECT * FROM question ORDER BY {o} DESC").format(o=sql.Identifier(order_by))
        cursor.execute(query)
    return cursor.fetchall()


def decode_timestamp(comment):
    for item in comment:
        item['submission_time'] = datetime.fromtimestamp(int(item['submission_time']))
    return comment


@connection.connection_handler
def filter_by_id(cursor: RealDictCursor, table, question_id, num='id'):
    if table == 'quest':
        query = """
                SELECT *
                FROM question
                WHERE question.id = %(q_id)s
                ORDER BY submission_time;
                """
        cursor.execute(query, {'q_id': question_id})
    else:
        query = """
                SELECT *
                FROM answer
                WHERE answer.question_id = %(q_id)s
                ORDER BY submission_time;
                """
        cursor.execute(query, {'q_id': question_id})

    return cursor.fetchall()


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


@connection.connection_handler
def add_question(cursor: RealDictCursor, title, message):
    # questions = connection.csv_to_list_of_dict("question.csv")
    # new_question = generate_question(questions, title, message)
    # questions.append(new_question)
    # connection.list_of_dict_to_csv(questions, "question.csv")
    # return new_question['id']
    query = """
            INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
            VALUES (date_trunc('minute', now()), 0, 0, %(title)s, %(msg)s, 'none')
            RETURNING id;
            """
    cursor.execute(query, {'title': title, 'msg': message})
    result = cursor.fetchone()
    return result['id']


@connection.connection_handler
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

