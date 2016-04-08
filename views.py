from flask import render_template, request
from app import app
from schedule_api import *

@app.route('/')
def index():
    data = {}
    data['terms'] = get_terms()
    return render_template('index.html', **data)
    
@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html'), 500 

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
def subject(term_code, school_code, subject_code):
    data = {}
    data['courses'] = get_catalog_numbers(term_code, school_code, subject_code)    
    
    return render_template('courses.html', **data)  
    
@app.route('/<term_code>/<school_code>/<subject_code>/<catalog_number>/')
def course(term_code, school_code, subject_code, catalog_number):
    data = {}
    data['course_description'] = get_course_description(term_code, school_code, 
                                    subject_code, catalog_number)
    data['course_sections'] = get_sections(term_code, school_code, 
                                    subject_code, catalog_number)
    data['course_title'] = subject_code + ' ' + catalog_number
        
    return render_template('course-info.html', **data)
    
@app.route('/<term_code>/<school_code>/<subject_code>/<catalog_number>/<section_number>/')
def section(term_code, school_code, subject_code, catalog_number, section_number):
    data = {}
    data['section_meetings'] = get_meetings(term_code, school_code, subject_code,
                                    catalog_number, section_number)
    data['section_details'] = get_section_details(term_code, school_code, 
                                    subject_code, catalog_number, section_number)
                                                    
    return render_template('section-details.html', **data)    
