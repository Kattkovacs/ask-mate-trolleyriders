from datetime import datetime

def decode_timestamp(list):
    for item in list:
        item['submission_time'] = datetime.fromtimestamp(int(item['submission_time']))
    return list

