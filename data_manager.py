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

