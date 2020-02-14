import connection
from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor


@connection.connection_handler
def firsts_from_list(cursor: RealDictCursor, order_by, order_direction) -> list:
    query = sql.SQL("SELECT * FROM question WHERE id < 6 ORDER BY {o} DESC ").format(o=sql.Identifier(order_by))
    cursor.execute(query)
    return cursor.fetchall()


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


@connection.connection_handler
def add_question_comment(cursor: RealDictCursor, question_id, message):
    query = """
            INSERT INTO comment (submission_time, edited_count, question_id, message)
            VALUES (date_trunc('minute', now()), 0, %(q_id)s, %(msg)s);
            """
    cursor.execute(query, {'q_id': question_id, 'msg': message})


@connection.connection_handler
def add_answer_comment(cursor: RealDictCursor, answer_id, message):
    query = """
            INSERT INTO comment (submission_time, edited_count, answer_id, message)
            VALUES (date_trunc('minute', now()), 0, %(q_id)s, %(msg)s);
            """
    cursor.execute(query, {'q_id': answer_id, 'msg': message})


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
def get_answer_id(cursor: RealDictCursor, qid):
    query = """
            SELECT id
            FROM answer
            WHERE answer.question_id = %(q_id)s;
            """
    cursor.execute(query, {'q_id': qid})
    return cursor.fetchall()


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
