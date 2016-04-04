import json
import time
import requests

class ScheduleApiError(Exception):
    '''
    Raised if there is an error with the schedule API.
    '''
    pass

# The base API endpoint
base_url = 'http://umich-schedule-api.herokuapp.com/v3'

# the amount of time to wait for the schedule API
timeout_duration = 25

def get_data(relative_path):
    '''
    Gets data from the schedule API at the specified path.
    Will raise a ScheduleApiError if unsuccessful.
    Assumes API will return JSON, returns as a dictionary.
    '''

    timeout_at = time.time() + timeout_duration

    while time.time() < timeout_at:
        r = requests.get(base_url + relative_path)
        if r.status_code == 200:
            return json.loads(r.text)
        if r.status_code == 400:
            break

    raise ScheduleApiError('error for url: {0} message: "{1}" code: {2}' \
        .format(relative_path, r.text, r.status_code))

def get_terms():
    '''
    Returns a list of valid terms.
    Each item in the list is a dictionary containing:
        ('TermCode', 'TermDescr', 'TermShortDescr')
    '''
    return get_data('/get_terms')

def get_schools(term_code):
    '''
    Returns a list of valid schools.
    Each item in the list is a dictionary containing:
        ('SchoolCode', 'SchoolDescr', 'SchoolShortDescr')
    '''
    return get_data('/get_schools?term_code=' + str(term_code))
    
def get_subjects(term_code, school_code):
    '''
    Returns a list of valid subjects.
    Each item in the list is a dictionary containing:
        ('SubjectShortDescr', 'SubjectCode', 'SubjectDescr')
    '''
    return get_data('/get_subjects?term_code=' + str(term_code) + 
                    '&school=' + school_code)
                    
def get_catalog_numbers(term_code, school_code, subject_code):
    '''
    Returns a list of valid subjects.
    Each item in the list is a dictionary containing:
        ('SubjectShortDescr', 'SubjectCode', 'SubjectDescr')
    '''
    return get_data('/get_catalog_numbers?term_code=' + str(term_code) + 
                    '&school=' + school_code + 
                    '&subject=' + subject_code)
                    
def get_course_description(term_code, school_code, subject_code, catalog_number):
    '''
    Returns a description for a valid course.
    ??? is this a single string
    '''
    return get_data('/get_course_description?term_code=' + str(term_code) + 
                    '&school=' + school_code + 
                    '&subject=' + subject_code + 
                    '&catalog_num=' + catalog_number)
              
def get_sections(term_code, school_code, subject_code, catalog_number):
    '''
    Returns a description for a valid course.
    Data structure appears to be a list of dicts.
    Each section returns a dict with ~13 key-var pairs.
    '''
    return get_data('/get_sections?term_code=' + str(term_code) + 
                    '&school=' + school_code + 
                    '&subject=' + subject_code + 
                    '&catalog_num=' + catalog_number)              


def get_section_details(term_code, school_code, subject_code, catalog_number, section_number):
    '''
    Returns section details for a valid course and section.
    Data structure is a dict with various key-var pairs, most of them
    are ints and strings. 
    "Instructors": is a list of dicts which contains string-string key-var pairs.
    '''
    return get_data('/get_sections?term_code=' + str(term_code) + 
                    '&school=' + school_code + 
                    '&subject=' + subject_code + 
                    '&catalog_num=' + catalog_number +
                    '&section_num=' + section_number)              
                    
                    
def get_meetings(term_code, school_code, subject_code, catalog_number, section_number): 
     ''' 
     Returns meeting times for a valid course and section. 
     ''' 
     return get_data('/get_meeting?term_code=' + str(term_code) +  
                     '&school=' + school_code +  
                    '&subject=' + subject_code +   
                    '&catalog_num=' + catalog_number + 
                    '&section_num=' + section_number)  


# TODO: implement "get_textbooks"
