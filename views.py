from flask import render_template, request
from app import app
from schedule_api import *

@app.route('/')
def index():
    data = {}
    data['terms'] = get_terms()
    return render_template('index.html', **data)

'''
You should add more functions below to "create pages" (each function preceded 
by '@app.route' represents a page) on your website.

	-	In addition to the information provided in the spec, use the index function
		above as a model for how you might setup the other functions.
	- 	Note some functions will need to have arguments (whereas index does not).
	- 	You may remove this comment when you start.
'''

@app.route('/term/<term_code>/')
def term(term_code):
    data = {}
    data['schools'] = get_schools(term_code)
    return render_template('schools.html', **data)
    
@app.route('/term/<term_code>/<school_code>/')
def school(term_code, school_code):
    data = {}
    data['subjects'] = get_subjects(term_code, school_code)
    return render_template('subjects.html', **data)    
    
@app.route('/term/<term_code>/<school_code>/<subject_code>/')
def course(term_code, school_code, subject_code):
    data = {}
    data['courses'] = get_courses(term_code, school_code, subject_code)
    return render_template('courses.html', **data)  