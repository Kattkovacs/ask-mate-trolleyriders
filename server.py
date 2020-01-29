from flask import Flask, render_template, request
import connection
import data_manager

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/list")
def list():
    questions = connection.csv_to_list_of_dict("question.csv")
    questions = data_manager.decode_timestamp(questions)
    return render_template("list.html", questions=questions)


@app.route("/question/<question_id>")
def question(question_id):
    questions = connection.csv_to_list_of_dict("question.csv")
    quest =  []
    questions = data_manager.decode_timestamp(questions)
    for item in questions:
        if item['id'] == question_id:
            quest.append(item)

    answers = connection.csv_to_list_of_dict("answer.csv")
    answ = []
    answers = data_manager.decode_timestamp(answers)
    for item in answers:
        if item['question_id'] == question_id:
            answ.append(item)
    return render_template("question.html", quest=quest, answ=answ)

@app.route("/add-question", methods=['GET', 'POST'])
def add_form():
    '''if request.method == 'POST':
        # we save the new note we got from the POST values
        saved_data['add'] = request.form['add']
        # we update how many times it has been edited
        saved_data['edit_count'] = saved_data.get('edit_count', 0) + 1

        # redirect to the home page which will show the saved note
        return redirect('/list')'''
    return render_template("add-question.html")

if __name__ == "__main__":
    app.run()
