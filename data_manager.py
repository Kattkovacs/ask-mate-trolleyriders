from flask import session

import connection
from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import bcrypt


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@connection.connection_handler
def users(cursor: RealDictCursor, email):
    query = """
            SELECT CASE WHEN EXISTS (SELECT user_name
            FROM user_data
            WHERE user_name = %(email)s)
            THEN 1
            ELSE 0 END;
            """
    cursor.execute(query, {'email': email})
    return cursor.fetchall()


@connection.connection_handler
def passwords(cursor: RealDictCursor, email):
    query = """
            SELECT password
            FROM user_data
            WHERE user_name = %(email)s;            
            """
    cursor.execute(query, {'email': email})
    result = cursor.fetchone()
    return result['password']


@connection.connection_handler
def firsts_from_list(cursor: RealDictCursor, order_by, order_direction) -> list:
    query = sql.SQL("SELECT * FROM question WHERE id < 6 ORDER BY {o} DESC ").format(o=sql.Identifier(order_by))
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_list(cursor: RealDictCursor, order_by, order_direction) -> list:
    if order_direction == 'asc':
        query = sql.SQL("SELECT * FROM question ORDER BY {o} ASC").format(o=sql.Identifier(order_by))
        cursor.execute(query)
    else:
        query = sql.SQL("SELECT * FROM question ORDER BY {o} DESC").format(o=sql.Identifier(order_by))
        cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_users_list(cursor: RealDictCursor, order_by, order_direction) -> list:
    if order_direction == 'asc':
        query = sql.SQL("SELECT * FROM user_data ORDER BY {o} ASC").format(o=sql.Identifier(order_by))
        cursor.execute(query)
    else:
        query = sql.SQL("SELECT * FROM user_data ORDER BY {o} DESC").format(o=sql.Identifier(order_by))
        cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def filter_by_id(cursor: RealDictCursor, table, question_id):
    if table == 'quest':
        query = """
                SELECT *
                FROM question
                WHERE question.id = %(q_id)s
                ORDER BY submission_time;
                """
        cursor.execute(query, {'q_id': question_id})

    elif table == 'answ':
        query = """
                SELECT *
                FROM answer
                WHERE answer.question_id = %(q_id)s
                ORDER BY submission_time DESC;
                """
        cursor.execute(query, {'q_id': question_id})

    elif table == 'answ_by_id':
        query = """
                SELECT *
                FROM answer
                WHERE answer.id = %(q_id)s
                ORDER BY submission_time DESC;
                """
        cursor.execute(query, {'q_id': question_id})

    elif table == 'comm_by_answ':
        query = """
                    SELECT *
                    FROM comment
                    WHERE comment.answer_id = %(q_id)s
                    ORDER BY submission_time DESC;
                    """
        cursor.execute(query, {'q_id': question_id})

    else:
        query = """
                    SELECT *
                    FROM comment
                    WHERE comment.question_id = %(q_id)s
                    ORDER BY submission_time DESC;
                    """
        cursor.execute(query, {'q_id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def add_user(cursor: RealDictCursor, user_name, password):
    query = """
            INSERT INTO user_data (user_name, password, registration_date, count_of_asked_questions, count_of_answers, count_of_comments, reputation, image)
            VALUES (%(user_name)s, %(password)s, date_trunc('minute', now()), 0, 0, 0, 0, 'none')
            RETURNING id;
            """
    cursor.execute(query, {'user_name': user_name, 'password': password})
    result = cursor.fetchone()
    return result['id']


@connection.connection_handler
def add_question(cursor: RealDictCursor, title, message, user):
    query = """
            INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
            VALUES (date_trunc('minute', now()), 0, 0, %(title)s, %(msg)s, 'none', %(uid)s)
            RETURNING id;
            """
    cursor.execute(query, {'title': title, 'msg': message, 'uid': user})
    result = cursor.fetchone()
    return result['id']


@connection.connection_handler
def add_answer(cursor: RealDictCursor, question_id, message, user):
    query = """
            INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id)
            VALUES (date_trunc('minute', now()), 0, %(q_id)s, %(msg)s, 'none', %(uid)s);
            """
    cursor.execute(query, {'q_id': question_id, 'msg': message, 'uid': user})


@connection.connection_handler
def add_question_comment(cursor: RealDictCursor, question_id, message, user):
    query = """
            INSERT INTO comment (submission_time, edited_count, question_id, message, user_id)
            VALUES (date_trunc('minute', now()), 0, %(q_id)s, %(msg)s, %(uid)s);
            """
    cursor.execute(query, {'q_id': question_id, 'msg': message, 'uid': user})


@connection.connection_handler
def add_answer_comment(cursor: RealDictCursor, answer_id, message, user):
    query = """
            INSERT INTO comment (submission_time, edited_count, answer_id, message, user_id)
            VALUES (date_trunc('minute', now()), 0, %(q_id)s, %(msg)s, %(uid)s);
            """
    cursor.execute(query, {'q_id': answer_id, 'msg': message, 'uid': user})


@connection.connection_handler
def select_qa(cursor: RealDictCursor, comment_id):
    query = """
            SELECT question_id, answer_id FROM comment
            WHERE comment.id = %(c_id)s;
            """
    cursor.execute(query, {'c_id': comment_id})
    return cursor.fetchall()


def get_question_details(question_id):
    question = filter_by_id('quest', question_id)[0]
    question['answers'] = filter_by_id('answ', question_id)
    question['comments'] = filter_by_id('comm', question_id)
    return question


@connection.connection_handler
def get_user_id(cursor: RealDictCursor, uid):
    query = """
            SELECT id
            FROM user_data
            WHERE user_data.user_name = %(us_nam)s;
            """
    cursor.execute(query, {'us_nam': uid})
    return cursor.fetchall()


# @connection.connection_handler
# def get_answer_id(cursor: RealDictCursor, qid):
#     query = """
#             SELECT id
#             FROM answer
#             WHERE answer.question_id = %(q_id)s;
#             """
#     cursor.execute(query, {'q_id': qid})
#     return cursor.fetchall()


@connection.connection_handler
def get_answer_question_id(cursor: RealDictCursor, aid):
    query = """
            SELECT question_id
            FROM answer
            WHERE id = %(a_id)s;
            """
    cursor.execute(query, {'a_id': aid})
    return cursor.fetchone()


@connection.connection_handler
def get_comment_question_id(cursor: RealDictCursor, aid):
    query = """
            SELECT question_id
            FROM comment
            WHERE id = %(a_id)s;
            """
    cursor.execute(query, {'a_id': aid})
    return cursor.fetchone()


@connection.connection_handler
def get_comment_answer_id(cursor: RealDictCursor, aid):
    query = """
            SELECT answer_id
            FROM comment
            WHERE id = %(a_id)s;
            """
    cursor.execute(query, {'a_id': aid})
    return cursor.fetchone()


@connection.connection_handler
def del_comment(cursor: RealDictCursor, cid):
    query = """
            DELETE FROM comment
            WHERE comment.id = %(c_id)s;
            """
    cursor.execute(query, {'c_id': cid})


@connection.connection_handler
def del_answer(cursor: RealDictCursor, aid):
    query = """
            DELETE FROM answer
            WHERE answer.id = %(a_id)s;
            """
    cursor.execute(query, {'a_id': aid})


@connection.connection_handler
def delete(cursor: RealDictCursor, qid):
    query = """
            DELETE FROM question
            WHERE question.id = %(q_id)s;
            """
    cursor.execute(query, {'q_id': qid})


@connection.connection_handler
def user_profile_list(cursor: RealDictCursor) -> list:
    query = """
        SELECT * FROM user_data
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def filter_by_user_id(cursor: RealDictCursor, table, user_id):
    if table == 'us':
        query = """
                SELECT *
                FROM user_data
                WHERE user_data.id = %(u_id)s
                """
        cursor.execute(query, {'u_id': user_id})
    return cursor.fetchall()

def get_user_details(user_id):
    user_by_id = filter_by_user_id('us', user_id)[0]
    return user_by_id