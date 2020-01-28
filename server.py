from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/list")
def list():
    return render_template("list.html")


if __name__ == "__main__":
    app.run()
