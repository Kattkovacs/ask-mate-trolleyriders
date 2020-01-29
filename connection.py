import os
import csv


dirname = os.path.dirname(__file__)

def csv_to_list_of_dict(file):
    with open(f"{dirname}/sample_data/{file}") as f:
        list_of_dict = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    return list_of_dict
