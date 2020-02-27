from flask import Flask, render_template, request, redirect, url_for, session
import data_manager

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/", methods=['GET'])
def index():
    questions = data_manager.firsts_from_list(request.args.get('order_by', default='submission_time'),
                                              request.args.get('order_direction', default='desc'))
    if 'user_name' in session:
        return render_template("index.html", questions=questions, email=session['user_name'])
    return render_template("index.html", questions=questions)


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        data_manager.add_user(request.form['user_name'], data_manager.hash_password(request.form['password']))
        return redirect(url_for('index'))
    return render_template("registration.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if not data_manager.users(request.form['user_name']) or not data_manager.verify_password(
                request.form['password'], data_manager.passwords(request.form['user_name'])):
            error = 'Wrong password!'
        else:
            session['user_name'] = request.form['user_name']
            return redirect(url_for('show_list'))
    return render_template("login.html", error=error)


@app.route("/list", methods=['GET', 'POST'])
def show_list():
    questions = data_manager.get_list(request.args.get('order_by', default='submission_time'),
                                      request.args.get('order_direction', default='desc'))
    if 'user_name' in session:
        user_id = data_manager.get_user_id(session['user_name'])[0]['id']
        return render_template("list.html", questions=questions, email=session['user_name'], user_id=user_id)
    return render_template("list.html", questions=questions)


@app.route("/question/<question_id>")
def question_page(question_id):
    question = data_manager.get_question_details(question_id)
    if 'user_name' in session:
        return render_template("question.html", question=question, email=session['user_name'])
    return render_template("question.html", question=question)


@app.route("/add-question", methods=['GET', 'POST'])
def add_form():
    """if request.method == 'POST':
        # we update how many times it has been edited
        saved_data['edit_count'] = saved_data.get('edit_count', 0) + 1"""
    if request.method == 'POST':
        new_q_id = data_manager.add_question(request.form['title'], request.form['message'], data_manager.get_user_id(session['user_name'])[0]['id'])
        return redirect(url_for('question_page', question_id=new_q_id))
    if 'user_name' in session:
        return render_template("add-question.html", email=session['user_name'])
    return redirect(url_for('login'))


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def new_answer(question_id):
    if request.method == 'POST':
        data_manager.add_answer(question_id, request.form['message'], data_manager.get_user_id(session['user_name'])[0]['id'])

    question = data_manager.filter_by_id('quest', question_id)[0]
    question['answers'] = data_manager.filter_by_id('answ', question_id)
    if 'user_name' in session:
        return render_template("new-answer.html", question=question, email=session['user_name'])
    return redirect(url_for('login'))


@app.route("/question/<question_id>/new-comment", methods=['GET', 'POST'])
def new_question_comment(question_id):
    if request.method == 'POST':
        data_manager.add_question_comment(question_id, request.form['message'], data_manager.get_user_id(session['user_name'])[0]['id'])

    question = data_manager.filter_by_id('quest', question_id)[0]
    question['comments'] = data_manager.filter_by_id('comm', question_id)
    if 'user_name' in session:
        return render_template("new-question-comment.html", question=question, email=session['user_name'])
    return redirect(url_for('login'))


@app.route("/answer/<answer_id>/new-comment", methods=['GET', 'POST'])
def new_answer_comment(answer_id):
    answer = data_manager.filter_by_id('answ_by_id', answer_id)[0]
    if request.method == 'POST':
        data_manager.add_answer_comment(answer_id, request.form['message'], data_manager.get_user_id(session['user_name'])[0]['id'])
    answer['comments'] = data_manager.filter_by_id('comm_by_answ', answer_id)
    if 'user_name' in session:
        return render_template("new-answer-comment.html", answer=answer, email=session['user_name'])
    return redirect(url_for('login'))


@app.route("/question/<question_id>/delete")
def delete(question_id):
    if 'user_name' in session:
        data_manager.delete(question_id)
        return redirect(url_for('show_list'))
    return redirect(url_for('login'))


@app.route("/answer/<answer_id>/delete")
def del_answer(answer_id):
    if 'user_name' in session:
        question_id = data_manager.get_answer_question_id(answer_id)['question_id']
        data_manager.del_answer(answer_id)
        return redirect(url_for('question_page', question_id=question_id))
    return redirect(url_for('login'))


@app.route("/comments/<comment_id>/delete")
def del_comment(comment_id):
    if 'user_name' in session:
        q_or_a = data_manager.select_qa(comment_id)
        data_manager.del_comment(comment_id)

        if q_or_a[0]['question_id'] is None:
            answer_id = q_or_a[0]['answer_id']
            return redirect(url_for('new_answer_comment', answer_id=answer_id))

        question_id = q_or_a[0]['question_id']
        return redirect(url_for('new_question_comment', question_id=question_id))
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    # flash("You are logged out")
    session.pop('user_name', None)
    return redirect(url_for('index'))


@app.route('/users', methods=['GET'])
def all_users():
    all_users_list = data_manager.get_users_list(request.args.get('order_by', default='registration_date'),
                                                 request.args.get('order_direction', default='desc'))
    if 'user_name' in session:
        return render_template("users.html", all_users_list=all_users_list, email=session['user_name'])
    return redirect(url_for('index'))


@app.route('/user/<user_id>')
def user_profile(user_id):
    user_by_id = data_manager.get_user_details(user_id)[0]
    if 'user_name' in session:
        return render_template("profile.html", user_by_id=user_by_id, email=session['user_name'])
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
