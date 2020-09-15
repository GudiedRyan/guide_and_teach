from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from guide_and_teach import db
from guide_and_teach.models import User, Course, Student, Grade
from guide_and_teach.grades.forms import GradeForm

grades = Blueprint('grades', __name__)

@grades.route('/course/<int:course_id>/student/<int:student_id>/add_grade', methods=['GET', 'POST'])
@login_required
def add_grade(course_id, student_id):
    student = Student.query.get_or_404(student_id)
    if student.user != current_user:
        abort(403)
    form = GradeForm()
    if form.validate_on_submit():
        grade = Grade(assignment=form.assignment.data, score=form.score.data, max_score=form.max_score.data, user=current_user, student=student)
        db.session.add(grade)
        db.session.commit()
        flash('Grade added!', 'success')
        return redirect(url_for('students.single_student', student_id=student.id, course_id=course_id))
    return render_template('grade.html', title="Add a new grade", form=form, legend="Add a new Grade")

@grades.route('/course/<int:course_id>/student/<int:student_id>/grade/<int:grade_id>/', methods=['GET', 'POST'])
@login_required
def single_grade(student_id, course_id, grade_id):
    grade = Grade.query.get_or_404(grade_id)
    if grade.user != current_user:
        abort(403)
    return render_template('single_grade.html', title="Grade", student_id=student_id, course_id=course_id, grade=grade)

@grades.route('/course/<int:course_id>/student/<int:student_id>/grade/<int:grade_id>/update', methods=['GET', 'POST'])
@login_required
def update_grade(student_id, course_id, grade_id):
    grade = Grade.query.get_or_404(grade_id)
    if grade.user != current_user:
        abort(403)
    form = GradeForm()
    if form.validate_on_submit():
        grade.assignment = form.assignment.data
        grade.score = form.score.data
        grade.max_score = form.max_score.data
        db.session.commit()
        flash('Changes have been saved!', 'success')
        return redirect(url_for('grades.single_grade', student_id=student_id, course_id=course_id, grade_id=grade_id))
    elif request.method == 'GET':
        form.assignment.data = grade.assignment
        form.score.data = grade.score
        form.max_score.data = grade.max_score
    return render_template('grade.html', title="Edit Grade Info", form=form, legend='Edit Grade Information')

@grades.route('/course/<int:course_id>/student/<int:student_id>/grade/<int:grade_id>/delete', methods=['POST'])
@login_required
def delete_grade(student_id, course_id, grade_id):
    grade = Grade.query.get_or_404(grade_id)
    if grade.user != current_user:
        abort(403)
    db.session.delete(grade)
    db.session.commit()
    flash('Grade has been deleted.', 'success')
    return redirect(url_for('students.single_student', course_id=course_id, student_id=student_id))
