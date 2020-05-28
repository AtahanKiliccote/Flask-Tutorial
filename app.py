from flask import Flask, render_template, url_for, request, redirect, session, flash
import flask_sqlalchemy
import sqlalchemy
#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
import datetime
dater = datetime.datetime.now()
dater_string = dater.strftime("%m/%d, %H:%M:%S")

app = Flask(__name__)
#sessions utorial
app.secret_key = "hello"
app.permanent_session_lifetime = datetime.timedelta(minutes=1)



#engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = flask_sqlalchemy.SQLAlchemy(app)
dbtasks = flask_sqlalchemy.SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

class tasks(dbtasks.Model):
    _id = dbtasks.Column("id", dbtasks.Integer, primary_key=True)
    t_tsk = dbtasks.Column("Task", dbtasks.String(100))
    t_length = dbtasks.Column("Length", dbtasks.String(100))
    t_date = dbtasks.Column("Date", dbtasks.String(100))
    #Action column that is functions delete() and update()

    def __init__(self, t_tsk, t_length, t_date):
        self.t_tsk = t_tsk
        self.t_length = t_length
        self.t_date = t_date
        #initialize the actions maybe idk


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view')
def view():
    return render_template("view.html", values=tasks.query.all())

@app.route('/task.html', methods=["POST", "GET"])
def task():
    if request.method == "POST":
        session.permanent= True
        tsk = request.form["tk"]
        length = request.form["len"]
        session["task"] = tsk
        session["length"] = length

        task_to_add = tasks(tsk, length, dater_string)
        
        #found_task = tasks.query.

        dbtasks.session.add(task_to_add)
        dbtasks.session.commit()

        flash("Task Added Successful!")  
        return render_template("task.html", values=tasks.query.all())
    else:
        return render_template("task.html", values=tasks.query.all())


@app.route("/login.html", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent= True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login Successful!")  
        return redirect(url_for("user"))
    else:
        if "user" in session:  
            flash("You're already logged in :))")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email Saved!")
        else:
            if "email" in session: 
                email = session["email"]

        return render_template("user.html", email=email)
    else: 
        return redirect(url_for("login.html"))

@app.route("/logout")
def logout():
    #if "user" in session:
    #    user = session["user"]
    #    flash("Logout Successful!, {user}", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

@app.route("/delete")
def delete():
    
    if dbtasks.session.query(tasks).count() == 0:
        flash("No Task to Delete!")
        return redirect(url_for("task"))

    for item in [dbtasks.session.query(tasks).count()]:
        dbtasks.session.delete(tasks.query.get(item))
    dbtasks.session.commit()
    flash("Task Deleted Successfully!")
    return redirect(url_for("task"))


if __name__== "__main__":
    db.create_all()
    dbtasks.create_all()
    app.run(debug=True)
 