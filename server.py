from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/list", methods=['GET', 'POST'])
def show_list():
    questions = data_manager.get_list("question.csv", request.args.get('order_by', default='submission_time'),
                                      request.args.get('order_direction', default='asc'))
    return render_template("list.html", questions=questions)


@app.route("/question/<question_id>")
def question_page(question_id):
    question = data_manager.filter_by_id("question.csv", question_id)
    answers = data_manager.filter_by_id("answer.csv", question_id, 'question_id')
    # question['answers'] = data_manager.sorting(answers)
    return render_template("question.html", question=question, answers=answers)


@app.route("/add-question", methods=['GET', 'POST'])
def add_form():
    """if request.method == 'POST':
        # we save the new note we got from the POST values
        saved_data['add'] = request.form['add']
        # we update how many times it has been edited
        saved_data['edit_count'] = saved_data.get('edit_count', 0) + 1

        # redirect to the home page which will show the saved note
        return redirect('/list')"""
    if request.method == 'POST' and request.form['message'] != '' and request.form['title'] != '':
        new_q_id = data_manager.add_question(request.form['title'], request.form['message'])
        return redirect(url_for('question_page', question_id=new_q_id))
    return render_template("add-question.html")


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def new_answer(question_id):
    question = data_manager.filter_by_id("question.csv", question_id)
    if request.method == 'POST' and request.form['message'] != '':
        data_manager.add_answer(question_id, request.form['message'])
    answers = data_manager.filter_by_id("answer.csv", question_id, 'question_id')

    return render_template("new-answer.html", question=question, answers=answers)


if __name__ == "__main__":
    app.run(debug=True)
