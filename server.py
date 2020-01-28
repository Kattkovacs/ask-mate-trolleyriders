from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)
dirname = os.path.dirname(__file__)


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/list")
def list(file=f"{dirname}/sample_data/question.csv"):
    with open(file) as q:
        questions = [{k: v for k, v in row.items()} for row in csv.DictReader(q, skipinitialspace=True)]
    return render_template("list.html", questions=questions)


if __name__ == "__main__":
    app.run()
