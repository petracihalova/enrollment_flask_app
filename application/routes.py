from application import app, db, ma
from flask import render_template, request, Response, json, redirect, flash, url_for, session, jsonify
from application.models import User, Course, Enrollment, courses_schema, course_schema
from application.forms import LoginForm, RegisterForm


@app.route("/api/courses")
def get_courses():
    courses_list = Course.query.all()
    result = courses_schema.dump(courses_list)
    return jsonify(result)


@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    email = data["email"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    password = data["password"]
    
    if User.query.filter_by(email=email).first():
        return jsonify(message=f"User already exists!"), 400

    new_user = User(email=email, first_name=first_name, last_name=last_name)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify(message=f"User {new_user.first_name} {new_user.last_name} sucessfully created!")



@app.route("/api/courses/<course_id>")
def get_course(course_id):
    course = Course.query.filter_by(course_id=course_id).first()
    result = course_schema.dump(course)
    return jsonify(result)


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("username"):
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            session["user_id"] = user.user_id
            session["username"] = user.first_name
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.", "danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/logout")
def logout():
    session["user_id"] = False
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/courses")
@app.route("/courses/<term>")
def courses(term=None):
    if term is None:
        term = "Spring 2023"

    classes = Course.query.order_by("course_id")
    return render_template("courses.html", course_data=classes, courses=True, term=term)


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("username"):
        return redirect(url_for("index"))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("You are successfully registered!", "success")
        return redirect("/index")

    return render_template("register.html", title="Registration", form=form, register=True)


@app.route("/enrollment", methods=["POST", "GET"])
def enrollment():
    if not session.get("username"):
        return redirect(url_for("login"))

    course_id = request.form.get("course_id")
    course_title = request.form.get("title")
    user_id = session.get("user_id")

    if course_id:
        if Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first():
            flash(f"Oops! You are already registered in this course {course_title}!", "danger")
            return redirect(url_for("courses"))
        else:
            enrollment = Enrollment(user_id=user_id, course_id=course_id)
            db.session.add(enrollment)
            db.session.commit()
            flash(f"You are enrolled in {course_title}!", "success")

    classes = Course.query.join(Enrollment).filter_by(user_id=user_id).order_by(Course.course_id)
    print(classes.count())
    term = request.form.get("term") 

    return render_template("enrollment.html", enrollment=True, title="Enrollment", classes=classes)
