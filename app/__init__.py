from flask import Flask, request, session, redirect, url_for, abort, render_template, flash

from app.model.user import User
from app.model.student import Student
from app.model import db
import os

try:
    from app.arpiths_shit_code import predict_sem1, predict_sem2, predict_sem3, predict_sem4
except Exception as e:
    # Dummy functions because fuck tensorflow no being released for python 3.7
    print("** Using dummy perdiction functions.")
    prediction = 3.5
    def predict_sem1(income, fos, english_score, previous_major, age, iset, prevgpa, sem1cre):
        return prediction

    def predict_sem2(income, fos, english_score, previous_major, age, leftwith1, iset, prevgpa, sem1cre, sem1gpa, sem2cre):
        return prediction

    def predict_sem3(age, income , fos, english_score, previous_major, leftwith1, leftwith2, iset, prevgpa, sem1cre, sem1gpa, sem2cre,sem2gpa,sem3cre):
        return prediction

    def predict_sem4(age, fos, english_score, previous_major, leftwith2, leftwith3, iset , prevgpa, sem1cre, sem1gpa, sem2cre, sem2gpa, sem3cre ,sem3gpa, sem4cre):
        return prediction

app = Flask(__name__)
app.config.from_object(__name__)    # Load config from this file

# Load default config and override config from an environtment variable
app.config.update(dict(
    SQLALCHEMY_ECHO = True,
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/test',
    SECRET_KEY = 'development key',
    USERNAME = 'admin',
    PASSWORD = 'default'
))
app.config.from_envvar('FOOBAR_SETTINGS', silent=True)
db.init_app(app)

@app.before_first_request
def initialize_database():
    print("\n\n\n...Initializing Database...\n\n\n")
    db.create_all()
    db.session.commit()
    return

@app.route('/')
def show_students():
    if not session.get('logged_in'):
        return render_template('login.html')
    students = Student.query.filter_by(user_id = session['user_id'])
    user = User.query.filter_by(id = session['user_id']).first()

    return render_template('show_students.html', user=user, entries=students)

@app.route('/user')
def show_user():
    user = None
    if session.get('logged_in'):
        # return render_template('login.html')
        user = User.query.filter_by(id = session['user_id']).first()
        return render_template('user.html', user=user, admin=False)

    elif session.get('admin_logged_in'):
        return render_template('user.html', user=user, admin=True)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username != app.config['USERNAME'] or password != app.config['PASSWORD']:
            error = 'invalid username or password'
        else:
            session['admin_logged_in'] = True
            flash('you were logged in as admin')
            return redirect('/')
    return render_template('admin_login.html', error=error, user=None)

# Create the student in the database
@app.route('/create_student', methods=["POST"])
def create_student():
    if not session.get('logged_in'):
        abort(401)

    new_student = Student(
        request.form['id'],
        session['user_id'],
        request.form['name'],
        request.form['email'],
        request.form['english_score'],
        request.form['year_ad'],
        request.form['total_credits'],
        request.form['nationality'],
        request.form['age'],
        request.form['prev_major'],
        request.form['prev_cgpa'],
        request.form['gender'],
        request.form['marital_status'],
        request.form['prev_institute'],
        request.form['fos']
        )
    db.session.add(new_student)
    db.session.commit()
    flash('new entry was successfully posted')
    return redirect(url_for('show_students'))

@app.route('/update_gpa')
def update_gpa():
    semester = int(request.args['sem'])
    gpa = request.args['gpa']
    student = Student.query.filter_by(id = request.args["student_id"]).first()

    if semester == 1:
        student.semester1_gpa_prediction = gpa
    elif semester == 2:
        student.semester2_gpa_prediction = gpa
    elif semester == 3:
        student.semester3_gpa_prediction = gpa
    elif semester == 4:
        student.semester4_gpa_prediction = gpa

    db.session.commit()
    return redirect("/student?student_id=%s" % (request.args["student_id"]))

@app.route('/student_graphs')
def show_student_graphs():
    student = Student.query.filter_by(id = request.args["student_id"]).first()
    user = User.query.filter_by(id = session['user_id']).first()
    return render_template('student_graphs.html', student=student, user=user)

@app.route('/graphs')
def show_graphs():
    user = User.query.filter_by(id = session['user_id']).first()
    return render_template('graphs.html', user=user)

# Update the student additional information.
@app.route('/update_student', methods=["POST"])
def update_student():
    student = Student.query.filter_by(id = request.form["id"]).first()

    student.semester1_credits   = request.form["semester1_credits"]
    student.semester1_gpa       = request.form["semester1_gpa"]
    student.left_with_1         = request.form["left_with_1"]
    student.semester2_credits   = request.form["semester2_credits"]
    student.semester2_gpa       = request.form["semester2_gpa"]
    student.fos                 = request.form['fos']

    student.left_with_2         = request.form["left_with_2"]
    student.semester3_credits   = request.form["semester3_credits"]
    student.semester3_gpa       = request.form["semester3_gpa"]

    student.left_with_3         = request.form["left_with_3"]
    student.semester4_credits   = request.form["semester4_credits"]
    student.semester4_gpa       = request.form["semester4_gpa"]
    student.cgpa                = request.form["cgpa"]
    student.id  		= request.form['id']
    student.name 		= request.form['name']
    student.email 		= request.form['email']
    student.english_score 	= request.form['english_score']
    student.admitted_year 	= request.form['year_ad']
    student.required_credits 	= request.form['total_credits']
    student.nationality  	= request.form['nationality']
    student.age 		= request.form['age']
    student.previous_major 	= request.form['prev_major']
    student.previous_cgpa 	= request.form['prev_cgpa']
    student.gender 		= request.form['gender']
    student.marital_status 	= request.form['marital_status']
    student.previous_institute  = request.form['prev_institute']

    student.semester1_credits 	= request.form['semester1_credits']
    student.semester1_gpa 	= request.form['semester1_gpa']

    student.left_with_1 	= request.form['left_with_1']
    student.semester2_credits 	= request.form['semester2_credits']
    student.semester2_gpa 	= request.form['semester2_gpa']

    student.left_with_2 	= request.form['left_with_2']
    student.semester3_credits 	= request.form['semester3_credits']
    student.semester3_gpa 	= request.form['semester3_gpa']

    student.left_with_3  	= request.form['left_with_3']
    student.semester4_credits 	= request.form['semester4_credits']
    student.semester4_gpa 	= request.form['semester4_gpa']
    student.cgpa 		= request.form['cgpa']

    db.session.commit()

    return redirect('?student_id=%s' % (student.id))

# Update the user additional information.
@app.route('/update_user', methods=["POST"])
def update_user():
    if request.args.get("id"):
        id = request.form["id"]
    elif session.get("user_id"):
        id = session["user_id"]
    else:
        id = -1
    user = User.query.filter_by(id = id).first()

    is_new_user = False
    if not user:
        is_new_user = True
        user = User(
                request.form['name'],
                request.form['username'],
                request.form['email'],
                request.form['fos'],
                request.form['password']
                )

    user.name     = request.form['name']
    user.username = request.form['username']
    user.email    = request.form['email']
    user.fos      = request.form['fos']

    if request.form['password']:
        user.hash_password(request.form['password'])

    user.upload_photo(app, request)

    if is_new_user:
        db.session.add(user)

    db.session.commit()

    return redirect('/user')

# Shows page to add a new student
@app.route('/add_student')
def add_student():
    if not session.get('logged_in'):
        return render_template('login.html')
    user = User.query.filter_by(id = session['user_id']).first()
    return render_template('add_student.html', user=user)

# Shows page to update additional student
@app.route('/add_info')
def add_info():
    if not session.get('logged_in'):
        return render_template('login.html')
    student = Student.query.filter_by(id = request.args["student_id"]).first()
    user = User.query.filter_by(id = session['user_id']).first()
    return render_template('add_info.html', student=student, user=user)

# Display a students information
@app.route('/student')
def student_page():
    if not session.get('logged_in'):
        return render_template('login.html')
    student = Student.query.filter_by(id = request.args["student_id"]).first()
    user = User.query.filter_by(id = session['user_id']).first()
    return render_template('student.html', student=student, user=user)

@app.route('/predict_sem1')
def predict_semester1():
    if not session.get('logged_in'):
        return render_template('login.html')
    student = Student.query.filter_by(id = request.args["student_id"]).first()

    lower_range = int(request.args["lower"])
    higher_range = int(request.args["higher"])

    predictions = []
    for i in range(lower_range, higher_range+1):
        prediction = float(predict_sem1(
                                student.nationality,
                                student.fos,
                                student.english_score,
                                student.previous_major,
                                student.age,
                                student.previous_institute,
                                student.previous_gpa,
                                i))
        eligibility = ""
        if(prediction >= 3.50): eligibility = "masters/phd"
        if(3.50 > prediction > 2.75): eligibility = "masters"
        if(prediction < 2.75): eligibility = "certificate"

        predictions.append({
            "credits": i,
            "gpa": round(prediction,2),
            "left_credits": int(student.required_credits) - i,
            "eligibility": eligibility
            })
    user = User.query.filter_by(id = session['user_id']).first()

    return render_template("prediction.html", predictions=predictions, sem_number=1, student=student, user=user)


@app.route('/predict_sem2')
def predict_semester2():
    if not session.get('logged_in'):
        return render_template('login.html')
    student = Student.query.filter_by(id = request.args["student_id"]).first()
    lower_range = int(request.args["lower"])
    higher_range = int(request.args["higher"])

    predictions = []
    for i in range(lower_range, higher_range+1):
        prediction = float(predict_sem2(
            student.nationality,
            student.fos,
            student.english_score,
            student.previous_major,
            student.age,
            student.left_with_1,
            student.previous_institute,
            student.previous_gpa,
            student.semester1_credits,
            student.semester1_gpa,
            i))
        eligibility = ""
        if ((2.75 < float(student.cgpa) < 3.5) and (prediction > 3.5)): eligibility = "masters, maybe phd"
        if ((2.75 < float(student.cgpa) < 3.5) and (2.75 < prediction < 3.5) ): eligibility = "research"
        if ((float(student.cgpa) < 2.75) and (2.75 < prediction < 3.5) ): eligibility = "maybe research / certificate"
        if ((float(student.cgpa) < 2.75) and (prediction < 2.75)): eligibility = "certificate"
        if ((float(student.cgpa) >= 3.5) and (prediction >= 3.5)): eligibility = "masters/phd"
        if ((float(student.cgpa) >= 3.5) and (2.75 < prediction <= 3.5)): eligibility = "masters/ maybe phd"
        predictions.append({
            "credits": i,
            "gpa": round(prediction,2),
            "left_credits": int(student.required_credits) - i - int(student.semester1_credits),
            "eligibility": eligibility
            })
    user = User.query.filter_by(id = session['user_id']).first()
    return render_template("prediction.html", predictions=predictions, sem_number=2, student=student, user=user)

@app.route('/predict_sem3')
def predict_semester3():
    if not session.get('logged_in'):
        return render_template('login.html')
    student = Student.query.filter_by(id = request.args["student_id"]).first()
    lower_range = int(request.args["lower"])
    higher_range = int(request.args["higher"])

    predictions = []
    for i in range(lower_range, higher_range+1):
        prediction = float(predict_sem3(
            student.age,
            student.nationality,
            student.fos,
            student.english_score,
            student.previous_major,
            student.left_with_1,
            student.left_with_2,
            student.previous_institute,
            student.previous_gpa,
            student.semester1_credits,
            student.semester1_gpa,
            student.semester2_credits,
            student.semester2_gpa,
            i))
        eligibility = ""
        if ((2.75 < flaot(student.cgpa) < 3.5) and (prediction > 3.5)): eligibility = "masters, maybe phd"
        if ((2.75 < float(student.cgpa) < 3.5) and (2.75 < prediction < 3.5) ): eligibility = "research"
        if ((float(student.cgpa) < 2.75) and (2.75 < prediction < 3.5) ): eligibility = "maybe research / certificate"
        if ((float(student.cgpa) < 2.75) and (prediction < 2.75)): eligibility = "certificate"
        if ((float(student.cgpa) >= 3.5) and (prediction >= 3.5)): eligibility = "masters/phd"
        if ((float(student.cgpa) >= 3.5) and (2.75 < prediction <= 3.5)): eligibility = "masters/ maybe phd"

        predictions.append({
            "credits": i,
            "gpa": round(prediction, 2),
            "left_credits": int(student.required_credits) - i - int(student.semester1_credits) - int(student.semester2_credits),
            "eligibility": eligibility
            })

    user = User.query.filter_by(id = session['user_id']).first()
    return render_template("prediction.html", predictions=predictions, sem_number=3, student=student, user=user)

@app.route('/predict_sem4')
def predict_semester4():
    if not session.get('logged_in'):
        return render_template('login.html')
    student = Student.query.filter_by(id = request.args["student_id"]).first()
    lower_range = int(request.args["lower"])
    higher_range = int(request.args["higher"])

    predictions = []
    for i in range(lower_range, higher_range+1):
        prediction = float(predict_sem4(
            student.age,
            student.fos,
            student.english_score,
            student.previous_major,
            student.left_with_2,
            student.left_with_3,
            student.previous_institute,
            student.previous_gpa,
            student.semester1_credits,
            student.semester1_gpa,
            student.semester2_credits,
            student.semester2_gpa,
            student.semester3_credits,
            student.semester3_gpa,
            i))

        predictions.append({
            "credits": i,
            "gpa": round(prediction, 2),
            "left_credits": int(student.required_credits) - i - int(student.semester1_credits) - int(student.semester2_credits) - int(student.semester3_credits)
            })


    user = User.query.filter_by(id = session['user_id']).first()
    return render_template("prediction.html", predictions=predictions, sem_number=4, student=student, user=user)

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()

        if ( not user ) or ( not user.verify_password(password) ):
            error = 'invalid username or password'
        else:
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = user.id
            flash('you were logged in')
            return redirect('/')
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('user_id', None)
    flash('you were logged out')
    return redirect(url_for('show_students'))

@app.route('/create_user', methods=["POST"])
def createUser():
    error = None
    data = request.get_json(True)

    user = User.query.filter_by(username = data["username"]).first()

    if not user:
        new_user = User(data["username"], data["email"], data["password"])
        db.session.add(new_user)
        db.session.commit()
        print("New user created.")
        flash('created new user')
    else:
        error = "User '%s' already exists" % (data["username"])

    return render_template('login.html', error=error)


if __name__ == "__main__":
    app.run(threaded=False)
