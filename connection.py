import os
import csv


dirname = os.path.dirname(__file__)

def csv_to_list_of_dict(file):
    with open(f"{dirname}/sample_data/{file}") as csvfile:
        list_of_dict = [{k: v for k, v in row.items()} for row in csv.DictReader(csvfile, skipinitialspace=True)]
    return list_of_dict


def list_of_dict_to_csv(list_of_dict, file):
    with open(f"{dirname}/sample_data/{file}", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(list_of_dict[0].keys()))
        writer.writeheader()
        for data in list_of_dict:
            writer.writerow(data)