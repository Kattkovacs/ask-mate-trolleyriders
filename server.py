from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/list", methods=['GET', 'POST'])
def show_list():
    print(request.args.get('order_by', default='submission_time'))
    questions = data_manager.get_list(request.args.get('order_by', default='submission_time'),
                                      request.args.get('order_direction', default='DESC'))
    return render_template("list.html", questions=questions)


@app.route("/question/<question_id>")
def question_page(question_id):
    question = data_manager.filter_by_id("question.csv", question_id)[0]
    question['answers'] = data_manager.filter_by_id("answer.csv", question_id, 'question_id')
    return render_template("question.html", question=question)


@app.route("/add-question", methods=['GET', 'POST'])
def add_form():
    """if request.method == 'POST':
        # we update how many times it has been edited
        saved_data['edit_count'] = saved_data.get('edit_count', 0) + 1"""
    if request.method == 'POST':
        new_q_id = data_manager.add_question(request.form['title'], request.form['message'])
        return redirect(url_for('question_page', question_id=new_q_id))
    return render_template("add-question.html")


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def new_answer(question_id):
    question = data_manager.filter_by_id("question.csv", question_id)[0]
    if request.method == 'POST':
        data_manager.add_answer(question_id, request.form['message'])
    question['answers'] = data_manager.filter_by_id("answer.csv", question_id, 'question_id')
    return render_template("new-answer.html", question=question)


@app.route("/question/<question_id>/delete")
def delete(question_id):
    data_manager.delete(question_id)
    return redirect(url_for('show_list'))

if __name__ == "__main__":
    app.run(debug=True)
