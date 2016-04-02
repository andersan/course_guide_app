from flask import render_template, request
from app import app
from schedule_api import *

@app.route('/')
def index():
    data = {}
    data['terms'] = get_terms()
    return render_template('index.html', **data)

@app.route('/<term_code>/')
def term(term_code):
    data = {}
    data['schools'] = get_schools(term_code)
    return render_template('schools.html', **data)
    
@app.route('/<term_code>/<school_code>/')
def school(term_code, school_code):
    data = {}
    data['subjects'] = get_subjects(term_code, school_code)
    return render_template('subjects.html', **data)    
    
@app.route('/<term_code>/<school_code>/<subject_code>/')
def course(term_code, school_code, subject_code):
    data = {}
    data['courses'] = get_courses(term_code, school_code, subject_code)
    return render_template('courses.html', **data)  