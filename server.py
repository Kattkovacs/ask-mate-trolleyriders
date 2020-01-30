from flask import Flask, render_template, request
import connection
import data_manager

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/list", methods=['GET', 'POST'])
def list():
    if request.method == 'POST':
        questions = connection.csv_to_list_of_dict("question.csv")
        newquestion = data_manager.generate_question(len(questions), request.form['title'], request.form['message'])
        questions.append(newquestion)
        connection.list_of_dict_to_csv(questions, "question.csv")
    questions = connection.csv_to_list_of_dict("question.csv")
    questions = data_manager.newest_first(questions)
    questions = data_manager.decode_timestamp(questions)

    return render_template("list.html", questions=questions)


@app.route("/question/<question_id>")
def question(question_id):
    questions = connection.csv_to_list_of_dict("question.csv")
    questions = data_manager.decode_timestamp(questions)
    questions = data_manager.filter_by_question_id(questions, question_id)

    answers = connection.csv_to_list_of_dict("answer.csv")
    answers = data_manager.decode_timestamp(answers)
    answers = data_manager.filter_by_question_id(answers, question_id, 'question_id')

    return render_template("question.html", questions=questions, answers=answers)

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


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def new_answer(question_id):
    questions = connection.csv_to_list_of_dict("question.csv")
    answers = connection.csv_to_list_of_dict("answer.csv")
    if request.method == 'POST':
        newanswer = data_manager.generate_answer(len(answers), question_id, request.form['message'])
        answers.append(newanswer)
        connection.list_of_dict_to_csv(answers, "answer.csv")


    questions = data_manager.decode_timestamp(questions)
    questions = data_manager.filter_by_question_id(questions, question_id)


    answers = data_manager.decode_timestamp(answers)
    answers = data_manager.filter_by_question_id(answers, question_id, 'question_id')

    return render_template("new-answer.html", questions=questions, answers=answers)



if __name__ == "__main__":
    app.run()
