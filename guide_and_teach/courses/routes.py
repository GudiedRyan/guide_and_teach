from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from guide_and_teach import db
from guide_and_teach.models import User, Course, Student
from guide_and_teach.courses.forms import CourseForm

courses = Blueprint('courses', __name__)

@courses.route('/course/new', methods=['GET', 'POST'])
@login_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(course_title=form.title.data, course_desc=form.description.data, user=current_user)
        db.session.add(course)
        db.session.commit()
        flash('Course created!', 'success')
        return redirect(url_for('courses.course_home'))
    return render_template('create_course.html', title='New Course', form=form, legend='Add a new course!')


@courses.route('/course/home')
@login_required
def course_home():
    courses = Course.query.all()
    return render_template('courses_page.html', title='Courses', courses=courses)
    

@courses.route('/course/<int:course_id>', methods=['GET','POST'])
@login_required
def single_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.user != current_user:
        abort(403)
    students = Student.query.all()
    return render_template('single_course.html', title='Course', course=course, students=students)

@courses.route('/course/<int:course_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('courses.single_course', course_id=course.id))
    elif request.method == 'GET':
        form.title.data = course.course_title
        form.description.data = course.course_desc
    return render_template('create_course.html', title="Update Course", form=form, legend='Make Changes')


@courses.route('/course/<int:course_id>/delete', methods=['POST'])
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.user != current_user:
        abort(403)
    db.session.delete(course)
    db.session.commit()
    flash('Your course has been deleted.', 'success')
    return redirect(url_for('courses.course_home'))
