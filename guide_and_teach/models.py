from flask import current_app
from guide_and_teach import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    course = db.relationship('Course', backref='user', lazy=True)
    student = db.relationship('Student', backref='user', lazy=True)
    grade = db.relationship('Grade', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(100), nullable=False)
    course_desc = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student = db.relationship('Student', backref='course', lazy=True)

    def __repr__(self):
        return f"Course('{self.course_title}')"

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    student_name = db.Column(db.String(50))
    teacher = db.relationship('User', backref="user")
    courses = db.relationship('Course', backref="course")
    grade = db.relationship('Grade', backref="student", lazy=True)

    def __repr__(self):
        return f"Student('{self.student_name}')"

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    score = db.Column(db.String(15), nullable=False)
    max_score = db.Column(db.String(15), nullable=False)
    assignment = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        return f"Grade('{self.score}', '{self.max_score}')"



# association table between student and user
# similar model to student, basically same idea

# class CourseList(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     student = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    # instructor = db.relationship('User', backref="user")
    # learner = db.relationship('Student', backref="student")