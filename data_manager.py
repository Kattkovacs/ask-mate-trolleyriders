import connection
from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor


@connection.connection_handler
def get_list(cursor: RealDictCursor, order_by, order_direction) -> list:
    if order_direction == 'ASC':
        query = sql.SQL("SELECT * FROM question ORDER BY {o} ASC").format(o=sql.Identifier(order_by))
        cursor.execute(query)
    else:
        query = sql.SQL("SELECT * FROM question ORDER BY {o} DESC").format(o=sql.Identifier(order_by))
        cursor.execute(query)
    return cursor.fetchall()


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
                ORDER BY submission_time DESC;
                """
        cursor.execute(query, {'q_id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def add_question(cursor: RealDictCursor, title, message):
    query = """
            INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
            VALUES (date_trunc('minute', now()), 0, 0, %(title)s, %(msg)s, 'none')
            RETURNING id;
            """
    cursor.execute(query, {'title': title, 'msg': message})
    result = cursor.fetchone()
    return result['id']


@connection.connection_handler
def add_answer(cursor: RealDictCursor, question_id, message):
    query = """
            INSERT INTO answer (submission_time, vote_number, question_id, message, image)
            VALUES (date_trunc('minute', now()), 0, %(q_id)s, %(msg)s, 'none');
            """
    cursor.execute(query, {'q_id': question_id, 'msg': message})





# def delete(question_id):
#     questions = connection.csv_to_list_of_dict("question.csv")
#     for question in questions:
#         if question['id'] == question_id:
#             questions.remove(question)
#     connection.list_of_dict_to_csv(questions, "question.csv")
#     answers = connection.csv_to_list_of_dict("answer.csv")
#     answers_left = []
#     for answer in answers:
#         if answer['question_id'] != question_id:
#             answers_left.append(answer)
#     connection.list_of_dict_to_csv(answers_left, "answer.csv")

