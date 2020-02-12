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
def filter_by_id(cursor: RealDictCursor, table, question_id):
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
            DELETE FROM comment
            WHERE comment.answer_id = %(a_id)s;
            DELETE FROM answer
            WHERE answer.id = %(a_id)s;
            """
    cursor.execute(query, {'a_id': aid})

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
def del_comment_by_answer_id(cursor: RealDictCursor, aid):
    query = """
            DELETE FROM comment
            WHERE comment.answer_id = %(a_id)s;
            """
    cursor.execute(query, {'a_id': aid})


@connection.connection_handler
def delete(cursor: RealDictCursor, qid):
    query = """
            DELETE FROM question_tag
            WHERE question_tag.question_id = %(q_id)s;
            DELETE FROM comment
            WHERE comment.question_id = %(q_id)s;
            DELETE FROM answer
            WHERE answer.question_id = %(q_id)s;
            DELETE FROM question
            WHERE question.id = %(q_id)s;
            """
    for item in get_answer_id(qid):
        del_comment_by_answer_id(item['id'])
    cursor.execute(query, {'q_id': qid})

