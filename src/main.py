from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
with sqlite3.connect("scores.db") as con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS scores(name TEXT, score INTEGER)")
    con.commit()


def get_best_score():
    with sqlite3.connect("scores.db") as con:
        cur = con.cursor()
        res = cur.execute(
            "SELECT name, score FROM scores ORDER BY score DESC LIMIT 1")
        best = res.fetchone()
        con.commit()
        print(best)
        return best


@app.route("/", methods=["GET"])
def index(name=None):
    if request.args.get("username") is None:
        best = get_best_score()
        return render_template("index.htm", best=best)
    else:
        score = 0
        answers = {
            "question1": "c",
            "question2": "a",
            "question3": "c",
            "question4": "b",
            "question5": "b",
            "question6": "b",
        }
        for key, value in answers.items():
            if request.args.get(key) == value:
                score += 1
        score /= len(answers)
        name = request.args.get("username")
        with sqlite3.connect("scores.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO scores VALUES (?, ?)", (name, score))
            con.commit()
        best = get_best_score()
        return render_template("result.htm", best=best, result=(name, score))
