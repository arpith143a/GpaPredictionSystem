from app.model import db
from passlib.apps import custom_app_context as pwd_context

class Student(db.Model):
    __tablename__ = 'student'
    id                  = db.Column(db.String(64), primary_key=True)
    user_id             = db.Column(db.Integer, nullable=False)
    name                = db.Column(db.String(64), nullable=False)
    email               = db.Column(db.String(64), nullable=False)
    english_score       = db.Column(db.String(64), nullable=False)
    admitted_year       = db.Column(db.String(64), nullable=False)
    required_credits    = db.Column(db.String(64), nullable=False)
    nationality         = db.Column(db.String(64), nullable=False)
    age                 = db.Column(db.String(64), nullable=False)
    previous_major      = db.Column(db.String(64), nullable=False)
    previous_gpa        = db.Column(db.String(64), nullable=False)
    previous_institute  = db.Column(db.String(64), nullable=False)
    gender              = db.Column(db.String(64), nullable=False)
    marital_status      = db.Column(db.String(64), nullable=False)
    fos                 = db.Column(db.String(64), nullable=False)

    semester1_credits   = db.Column(db.String(64), nullable=True)
    semester1_gpa       = db.Column(db.String(64), nullable=True)

    left_with_1         = db.Column(db.String(64), nullable=True)
    semester2_credits   = db.Column(db.String(64), nullable=True)
    semester2_gpa       = db.Column(db.String(64), nullable=True)

    left_with_2         = db.Column(db.String(64), nullable=True)
    semester3_credits   = db.Column(db.String(64), nullable=True)
    semester3_gpa       = db.Column(db.String(64), nullable=True)

    left_with_3         = db.Column(db.String(64), nullable=True)
    semester4_credits   = db.Column(db.String(64), nullable=True)
    semester4_gpa       = db.Column(db.String(64), nullable=True)
    cgpa                = db.Column(db.String(64), nullable=True)


    semester1_gpa_prediction = db.Column(db.String(64), nullable=True)
    semester2_gpa_prediction = db.Column(db.String(64), nullable=True)
    semester3_gpa_prediction = db.Column(db.String(64), nullable=True)
    semester4_gpa_prediction = db.Column(db.String(64), nullable=True)

    def __init__(self,
                id,
                user_id = "",
                name="",
                email="",
                english_score="",
                admitted_year="",
                required_credits="",
                nationality="",
                age="",
                previous_major="",
                previous_gpa="",
                gender="",
                marital_status="",
                previous_institute="",
                fos="",
                **kwargs):
        self.id                  = id
        self.user_id             = user_id
        self.name                = name
        self.email               = email
        self.english_score       = english_score
        self.admitted_year       = admitted_year
        self.required_credits    = required_credits
        self.nationality         = nationality
        self.age                 = age
        self.previous_major      = previous_major
        self.previous_gpa        = previous_gpa
        self.gender              = gender
        self.marital_status      = marital_status
        self.previous_institute  = previous_institute
        self.fos                 = fos

        self.semester1_credits   = ""
        self.semester1_gpa       = ""
        self.left_with_1         = ""
        self.semester2_credits   = ""
        self.semester2_gpa       = ""
        self.left_with_2         = ""
        self.semester3_credits   = ""
        self.semester3_gpa       = ""
        self.left_with_3         = ""
        self.semester4_credits   = ""
        self.semester4_gpa       = ""
        self.cgpa                = ""
