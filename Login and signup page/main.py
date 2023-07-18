from flask import Flask, request, render_template, url_for, redirect, flash
import sqlite3
conn = sqlite3.connect("new.db", check_same_thread=False)
cr = conn.cursor()
conn.execute("create table if not exists student(name varchar, password varchar, course varchar)")

app = Flask(__name__)

app.secret_key = "Gopi"

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        uname = request.form["uname"]
        upass = request.form["upass"]
        cr.execute("select * from student where name = ? ", (uname,))
        res = cr.fetchone()

        if res is None:
            flash("Invaild Username....", "danger")
            return redirect(url_for('home'))
        elif upass not in res:
            flash("Invaild password....", "danger")
            return redirect(url_for('home'))
        else:
            flash("Login successfully...", "success")
            return redirect(url_for('home'))
    return render_template("index.html")

@app.route('/login')
def login():
    conn = sqlite3.connect("new.db")
    conn.row_factory = sqlite3.Row
    cr = conn.cursor()
    cr.execute("select * from student")
    res = cr.fetchall()
    conn.close()
    return render_template("login.html",res=res)

@app.route("/signup page", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        uname = request.form.get("uname")
        upass = request.form["upass"]
        ucourse = request.form["ucourse"]
        conn.execute("insert into student values(?, ?, ?)", (uname, upass, ucourse))
        conn.commit()

        return redirect(url_for("home"))
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)