import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from guide_and_teach import app, db, bcrypt
from guide_and_teach.forms import RegistrationForm, LoginForm, CourseForm, StudentForm
from guide_and_teach.models import User, Course, Student
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template('about.html', title='About Page')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('course_home'))
        else:
            flash('Login failed. Check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/course/new', methods=['GET', 'POST'])
@login_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(course_title=form.title.data, course_desc=form.description.data, user=current_user)
        db.session.add(course)
        db.session.commit()
        flash('Course created!', 'success')
        return redirect(url_for('course_home'))
    return render_template('create_course.html', title='New Course', form=form, legend='Add a new course!')


@app.route('/course/home')
@login_required
def course_home():
    courses = Course.query.all()
    return render_template('courses_page.html', title='Courses', courses=courses)
    

@app.route('/course/<int:course_id>', methods=['GET','POST'])
@login_required
def single_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.user != current_user:
        abort(403)
    students = Student.query.all()
    return render_template('single_course.html', title='Course', course=course, students=students)

@app.route('/course/<int:course_id>/update', methods=['GET', 'POST'])
@login_required
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.user != current_user:
        abort(403)
    form = CourseForm()
    if form.validate_on_submit():
        course.course_title = form.title.data
        course.course_desc = form.description.data
        db.session.commit()
        flash('Changes have been saved!', 'success')
        return redirect(url_for('single_course', course_id=course.id))
    elif request.method == 'GET':
        form.title.data = course.course_title
        form.description.data = course.course_desc
    return render_template('create_course.html', title="Update Course", form=form, legend='Make Changes')


@app.route('/course/<int:course_id>/delete', methods=['POST'])
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.user != current_user:
        abort(403)
    db.session.delete(course)
    db.session.commit()
    flash('Your course has been deleted.', 'success')
    return redirect(url_for('course_home'))
@app.route('/course/<int:course_id>/add_student', methods = ['GET', 'POST'])
@login_required
def add_student(course_id):
    course = Course.query.get_or_404(course_id)
    if course.user != current_user:
        abort(403)
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(student_name=form.student_name.data, user=current_user, course=course)
        db.session.add(student)
        db.session.commit()
        flash('Student Added!', 'success')
        return redirect(url_for('single_course', course_id=course.id))
    return render_template('student.html', title="Add Student", form=form, legend="Add a Student")

@app.route('/course/student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def single_student(student_id):
    student = Student.query.get_or_404(student_id)
    if student.user != current_user:
        abort(403)
    return render_template('single_student.html', title="student.student_name", student=student)

@app.route('/course/student/<int:student_id>/delete', methods=['POST'])
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    if student.user != current_user:
        abort(403)
    db.session.delete(student)
    db.session.commit()
    flash('Your course has been deleted.', 'success')
    return redirect(url_for('course_home'))