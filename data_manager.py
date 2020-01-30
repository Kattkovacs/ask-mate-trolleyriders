from datetime import datetime


def decode_timestamp(list):
    for item in list:
        item['submission_time'] = datetime.fromtimestamp(int(item['submission_time']))
    return list


def filter_by_question_id(list, question_id, id='id'):
    filtered = []
    for item in list:
        if item[id] == question_id:
            filtered.append(item)
    return filtered


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

