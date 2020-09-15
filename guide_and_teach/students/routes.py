from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from guide_and_teach import db
from guide_and_teach.models import User, Course, Student, Grade
from guide_and_teach.students.forms import StudentForm

students = Blueprint('students', __name__)

@students.route('/course/<int:course_id>/add_student', methods = ['GET', 'POST'])
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
        return redirect(url_for('courses.single_course', course_id=course.id))
    return render_template('student.html', title="Add Student", form=form, legend="Add a Student")

@students.route('/course/<int:course_id>/student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def single_student(student_id, course_id):
    student = Student.query.get_or_404(student_id)
    if student.user != current_user:
        abort(403)
    grades = Grade.query.all()
    return render_template('single_student.html', title="Student", student=student, course_id=course_id, grades=grades)

@students.route('/course/<int:course_id>/student/<int:student_id>/delete', methods=['POST'])
@login_required
def delete_student(student_id, course_id):
    student = Student.query.get_or_404(student_id)
    if student.user != current_user:
        abort(403)
    db.session.delete(student)
    db.session.commit()
    flash('Student has been deleted.', 'success')
    return redirect(url_for('courses.single_course', course_id=course_id))

@students.route('/course/<int:course_id>/student/<int:student_id>/update', methods=['GET', 'POST'])
@login_required
def update_student(student_id, course_id):
    student = Student.query.get_or_404(student_id)
    if student.user != current_user:
        abort(403)
    form = StudentForm()
    if form.validate_on_submit():
        student.student_name = form.student_name.data
        db.session.commit()
        flash('Changes have been saved!', 'success')
        return redirect(url_for('students.single_student', student_id=student.id, course_id=course_id))
    elif request.method == 'GET':
        form.student_name.data = student.student_name
    return render_template('student.html', title="Update Student Info", form=form, legend='Make Changes')
