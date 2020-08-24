from guide_and_teach import db, app, login_manager
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

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # student = db.relationship('Student', backref='course', lazy=True)

    def __repr__(self):
        return f"Course('{self.course_title}')"









# class Student(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     student_name = db.Column(db.String(100), nullable=False)
#     course_id = db.Column(db.Integer, db.ForeignKey('course.user_id'), nullable=False)
#     grades = db.relationship('Grade', backref='student', lazy=True)

#     def __repr__(self):
#         return f"Student('{self.student_name}')"

# class Grade(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     earned_grade = db.Column(db.Integer, nullable=False)
#     max_grade = db.Column(db.Integer, nullable=False)
#     student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

#     def __repr__(self):
#         return f"Grade('{self.earned_grade}', '{self.max_grade}')"

