from flask import Flask, render_template, request
import csv
import os
from datetime import datetime

app = Flask(__name__)
dirname = os.path.dirname(__file__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/list")
def list():
    with open(f"{dirname}/sample_data/question.csv") as q:
        questions = [{k: v for k, v in row.items()} for row in csv.DictReader(q, skipinitialspace=True)]
        for item in questions:
            item['submission_time'] = datetime.fromtimestamp(int(item['submission_time']))
    return render_template("list.html", questions=questions)


@app.route("/question/<question_id>")
def question(question_id):
    with open(f"{dirname}/sample_data/question.csv") as q:
        questions = [{kq: vq for kq, vq in rowq.items()} for rowq in csv.DictReader(q, skipinitialspace=True)]
        quest =  []
        for item in questions:
            item['submission_time'] = datetime.fromtimestamp(int(item['submission_time']))
            if item['id'] == question_id:
                quest.append(item)

    with open(f"{dirname}/sample_data/answer.csv") as a:
        answers = [{ka: va for ka, va in rowa.items()} for rowa in csv.DictReader(a, skipinitialspace=True)]
        answ = []
        for item in answers:
            item['submission_time'] = datetime.fromtimestamp(int(item['submission_time']))
            if item['question_id'] == question_id:
                answ.append(item)
    return render_template("question.html", quest=quest, answ=answ)


if __name__ == "__main__":
    app.run()
