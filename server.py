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
    # sorted(x.items(), key=lambda item: item[1])

if __name__ == "__main__":
    app.run()
