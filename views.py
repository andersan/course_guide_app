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
    data['selected_term'] = term_code
    data['schools'] = get_schools(term_code)
    return render_template('schools.html', **data)
    
@app.route('/<term_code>/<school_code>/')
def school(term_code, school_code):
    data = {}
    data['selected_term'] = term_code
    data['selected_school'] = school_code
    data['subjects'] = get_subjects(term_code, school_code)
    return render_template('subjects.html', **data)    
    
@app.route('/<term_code>/<school_code>/<subject_code>/')
def subject(term_code, school_code, subject_code):
    data = {}
    data['selected_term'] = term_code
    data['selected_school'] = school_code
    data['selected_subject'] = subject_code
    data['courses'] = get_catalog_numbers(term_code, school_code, subject_code)    
    return render_template('courses.html', **data)  
    
@app.route('/<term_code>/<school_code>/<subject_code>/<catalog_number>/')
def course(term_code, school_code, subject_code, catalog_number):
    data = {}
    data['selected_term'] = term_code
    data['selected_school'] = school_code
    data['selected_subject'] = subject_code
    data['selected_course'] = catalog_number
    data['courses'] = get_catalog_numbers(term_code, school_code, subject_code)  
    data['course_description'] = get_course_description(term_code, school_code, 
                                    subject_code, catalog_number)
    data['course_sections'] = get_sections(term_code, school_code, 
                                    subject_code, catalog_number)
    data['course_title'] = subject_code + ' ' + catalog_number
    return render_template('course-info.html', **data)
    
@app.route('/<term_code>/<school_code>/<subject_code>/<catalog_number>/<section_number>/')
def section(term_code, school_code, subject_code, catalog_number, section_number):
    data = {}
    data['selected_term'] = term_code
    data['selected_school'] = school_code
    data['selected_subject'] = subject_code
    data['selected_course'] = catalog_number
    data['selected_section'] = section_number
    data['courses'] = get_catalog_numbers(term_code, school_code, subject_code) 
    data['course_sections'] = get_sections(term_code, school_code, 
                                    subject_code, catalog_number)
    data['section_meetings'] = get_meetings(term_code, school_code, subject_code,
                                    catalog_number, section_number)
    data['section_details'] = get_section_details(term_code, school_code, 
                                    subject_code, catalog_number, section_number)
    data['section_location'] = get_meetings(term_code, school_code, subject_code,
                                    catalog_number, section_number)[0]['Location']

# building abbreviations from the office of the registrar

# concerns with location dict: DENT (renamed to Weiser), buildings that are not in Ann Arbor, names with apostrophes, locations that still need to be arranged

    data['building_locations'] = {
    'A&AB': 'Art and Architecture Building',
    'AH': 'Angell Hall',
    'AL': 'Walter E. Lay Automotive Lab',
    'ALH': 'Alice Lloyd Hall',
    'ANNEX': 'Public Policy Annex, 1015 E. Huron',
    'ARGUS2': 'Argus Building II, Television Center, 408 S. Fourth Street',
    'ARGUS3': 'Argus Building III, 416 S. Fourth Street',
    'ARR': 'Location to be Arranged',
    'BAM HALL': 'Blanch Anderson Moore Hall, School of Music',
    'BELL POOL': 'Margaret Bell Pool, Central Campus Recreation Building',
    'BEYST': 'Bob and Betty Beyster Building',
    'BIOL STAT': 'Biological Station, Pellston',
    'BMT': 'Burton Memorial Tower',
    'BOT GARD': 'Matthaei Botanical Gardens, Dixboro Road',
    'BSRB': 'Biomedical Science Research Building',
    'BURS': 'Bursley Hall',
    'BUS': 'Business Administration',
    'CAMP DAVIS': 'Camp Davis, Jackson Hole, Wyoming',
    'CCL': 'Clarence Cook Little Building',
    'CCRB': 'Central Campus Recreation Building',
    'CHEM': 'Chemistry Building',
    'CHRYS': 'Chrysler Center',
    'COMM PARK': 'Commerce Park, Dearborn', #unsure where this is
    'COOL': 'Cooley Building',
    'COUZENS': 'Couzens Hall',
    'CPH': 'Children\'s Psychiatric Hospital',
    'CRISLER': 'Crisler Arena',
    'CCSB': 'Campus Safety Services Building, 1239 Kipke Dr.',
    'DANA': 'Dana Building (School of Natural Resources and Environment)',
    'DANCE': 'Dance Building, 1310 N. University Court',
    'DC': 'Duderstadt Center',
    'DENN': 'David M. Dennison Building (Weiser Hall)',
    'DENT': 'Dental Building',
    'DOW': 'Dow Engineering Building',
    'E-BUS': 'Executive Education',
    'EECS': 'Electrical Engineering and Computer Science Building',
    'EH': 'East Hall',
    'EQ': 'East Quadrangle',
    'ERB1': 'Engineering Research Building 1',
    'ERB2': 'Engineering Research Building 2',
    'EWRE': 'Environmental and Water Resources Engineering Building',
    'FA CAMP': 'Fresh Air Camp, Pinckney', # is this correct??
    'FORD LIB': 'Ford Library',
    'FXB': 'Francois-Xavier Bagnoud Building',
    'GFL': 'Gorguze Family Laboratory',
    'GGBL': 'G. G. Brown Laboratory',
    'GLIBN': 'Harlan Hatcher Graduate Library',
    'HH': 'Haven Hall',
    'HUTCH': 'Hutchins Hall',
    'IM POOL': 'Intramural Building',
    'IOE': 'Industrial and Operations Engineering Building',
    'ISR': 'Institute for Social Research',
    'K-BUS': 'Kresge Library',
    'KEC': 'Kellogg Eye Center',
    'KEENE THTR EQ': 'Keene Theater, Residential College, East Quadrangle',
    'KELSEY': 'Kelsey Museum of Archaeology',
    'KHRI': 'Kresge Hearing Research Institute',
    'LANE': 'Lane Hall',
    'LBME': 'Lurie Biomedical Engineering Building',
    'LEAG': 'Michigan League',
    'LEC': 'Lurie Engineering Center',
    'LLIB': 'Law Library',
    'LORCH': 'Lorch Hall',
    'LSA': 'Literature, Science, and the Arts Building',
    'LSI': 'Life Sciences Institute',
    'LSSH': 'Law School South Hall',
    'MARKLEY': 'Mary Markley Hall',
    'MAX KADE': 'Max Kade House, 627 Oxford Street',
    'MH': 'Mason Hall',
    'MHRI': 'Mental Health Research Institute',
    'MLB': 'Modern Languages Building',
    'MONROECTY HD': 'Monroe County Health Department',
    'MOSHER': 'Mosher Jordan Hall',
    'MOTT': 'C.S. Mott Children\'s Hospital',
    'MSC1': 'Medical Science, Building I',
    'MSC2': 'Medical Science, Building II',
    'MSRB3': 'Medical Science Research, Building III',
    'NAME': 'Naval Architecture and Marine Engineering Building',
    'NCRB': 'North Campus Recreation Building',
    'NCRC': 'North Campus Research Complex',
    'NIB': '300 North Ingalls Building',
    '400NI': '400 North Ingalls Building',
    'NORTHVILLEPH': 'Northville State Hospital',
    'NQ': 'North Quad',
    'NS': 'Edward Henry Kraus Natural Science Building',
    'OBL': 'Observatory Lodge, 1402 Washington Heights',
    'PALM': 'Palmer Commons',
    'PHOENIXLAB': 'Phoenix Memorial Laboratory',
    'PIER': 'Pierpont Commons',
    'POWER CTR': 'Power Center for Performing Arts',
    'RACK': 'Horace H. Rackham, School of Graduate Studies',
    'RAND': 'Randall Laboratory',
    'R-BUS': 'Ross School of Business Building',
    'REVELLI': 'William D. Revelli Hall',
    'ROSS AC': 'Stephen M. Ross Academic Center',
    'RUTHVEN': 'A. G. Ruthven Museums Building',
    'SCHEM': 'Glenn E. Schembechler Hall',
    'SEB': 'School of Education Building',
    'SHAPIRO': 'Shapiro Undergraduate Library',
    'SM': 'Earl V. Moore Building, School of Music',
    'SNB': 'School of Nursing Building',
    'SNRE': 'Dana Samuel Trask Building (School of Natural Resources and Environment)', #FIX
    'SPH1': 'Henry Vaughan Building',
    'SPH2': 'Thomas Francis, Jr Building',
    'SRB': 'Space Research Building',
    'STB': '202 South Thayer Building',
    'STJOSEPH HOSP': 'St. Joseph Mercy Hospital',
    'STOCKWELL': 'Stockwell Hall',
    'STRNS': 'Sterns Building',
    'T&TB': 'Track and Tennis Building',
    'TAP': 'Tappan Hall',
    'TAUBL': 'Learning Resource Center, Taubman Medical Library',
    'TISCH': 'Tisch Hall',
    'UM HOSP': 'University Hospital Medical Campus',
    'UMMA': 'University of Michigan Museum of Art (Alumni Memorial Hall)',
    'UNION': 'Michigan Union',
    'USB': 'Undergraduate Science Building',
    'UTOWER': 'University Towers, 1225 S. University',
    'VETERANSHOSP': 'Veterans Administration Hospital',
    'WASHCTY HD': 'Washtenaw County Health Department',
    'W-BUS': 'Wyly Hall',
    'WDC': 'Charles R. Walgreen, Jr. Drama Center',
    'WEILL': 'Joan and Sanford Weill Hall',
    'WEIS': 'Weiser Hall',
    'WH': 'West Hall',
    'WOMEN\'S HOSP': 'Women\'s Hospital',
    'WQ': 'West Quad',
}
                                                    
    return render_template('section-details.html', **data)  

@app.route('/about-us.html/')
def about():
    data = {}
    return render_template('about-us.html', **data)  

@app.route('/test.html')
def test():
    data = {}
    data['building_locations'] = {
    'A&AB': 'Art and Architecture Building', #fix
    'AH': 'Angell Hall',
    'AL': 'Walter E. Lay Automotive Lab',
    'ALH': 'Alice Lloyd Hall',
    'ANNEX': 'Public Policy Annex, 1015 E. Huron',
    'ARGUS2': 'Argus Building II, Television Center, 408 S. Fourth Street', #fix
    'ARGUS3': 'Argus Building III, 416 S. Fourth Street',
    'ARR': 'Location to be Arranged',
    'BAM HALL': 'Blanch Anderson Moore Hall, School of Music', #FIX
    'BELL POOL': 'Margaret Bell Pool, Central Campus Recreation Building', #FIX
    'BEYST': 'Bob and Betty Beyster Building',
    'BIOL STAT': 'Biological Station, Pellston', #FIX: one in pellston
    'BMT': 'Burton Memorial Tower',
    'BOT GARD': 'Matthaei Botanical Gardens, Dixboro Road',
    'BSRB': 'Biomedical Science Research Building',
    'BURS': 'Bursley Hall',
    'BUS': 'Business Administration',
    'CAMP DAVIS': 'Camp Davis, Jackson Hole, Wyoming', #FIX
    'CCL': 'Clarence Cook Little Building',
    'CCRB': 'Central Campus Recreation Building',
    'CHEM': 'Chemistry Building', #WIllard henry dow lab ok?
    'CHRYS': 'Chrysler Center', #FIX: 2121 Bonisteel Blvd
    'COMM PARK': 'Commerce Park, Dearborn', #FIX: 15041 S Commerce Dr. Dearborn, MI 48120
    'COOL': 'Cooley Building',
    'COUZENS': 'Couzens Hall',
    'CPH': 'Children\'s Psychiatric Hospital',
    'CRISLER': 'Crisler Arena',
    'CCSB': 'Campus Safety Services Building, 1239 Kipke Dr.',
    'DANA': 'Dana Building (School of Natural Resources and Environment)', #FIX
    'DANCE': 'Dance Building, 1310 N. University Court',
    'DC': 'Duderstadt Center',
    'DENN': 'David M. Dennison Building (Weiser Hall)',
    'DENT': 'Dental Building',
    'DOW': 'Dow Engineering Building',
    'E-BUS': 'Executive Education',
    'EECS': 'Electrical Engineering and Computer Science Building',
    'EH': 'East Hall',
    'EQ': 'East Quadrangle',
    'ERB1': 'Engineering Research Building 1',
    'ERB2': 'Engineering Research Building 2',
    'EWRE': 'Environmental and Water Resources Engineering Building', #FIX
    'FA CAMP': 'Fresh Air Camp, Pinckney', #FIX
    'FORD LIB': 'Ford Library',
    'FXB': 'Francois-Xavier Bagnoud Building',
    'GFL': 'Gorguze Family Laboratory',
    'GGBL': 'G. G. Brown Laboratory',
    'GLIBN': 'Harlan Hatcher Graduate Library',
    'HH': 'Haven Hall',
    'HUTCH': 'Hutchins Hall',
    'IM POOL': 'Intramural Building',
    'IOE': 'Industrial and Operations Engineering Building',
    'ISR': 'Institute for Social Research',
    'K-BUS': 'Kresge Library',
    'KEC': 'Kellogg Eye Center',
    'KEENE THTR EQ': 'Keene Theater, Residential College, East Quadrangle',
    'KELSEY': 'Kelsey Museum of Archaeology',
    'KHRI': 'Kresge Hearing Research Institute', #FIX
    'LANE': 'Lane Hall',
    'LBME': 'Lurie Biomedical Engineering Building',
    'LEAG': 'Michigan League',
    'LEC': 'Lurie Engineering Center',
    'LLIB': 'Law Library', #FIX
    'LORCH': 'Lorch Hall',
    'LSA': 'Literature, Science, and the Arts Building',
    'LSI': 'Life Sciences Institute',
    'LSSH': 'Law School South Hall',
    'MARKLEY': 'Mary Markley Hall',
    'MAX KADE': 'Max Kade House, 627 Oxford Street', #FIX
    'MH': 'Mason Hall',
    'MHRI': 'Mental Health Research Institute',
    'MLB': 'Modern Languages Building',
    'MONROECTY HD': 'Monroe County Health Department', #FIX
    'MOSHER': 'Mosher Jordan Hall',
    'MOTT': 'C.S. Mott Children\'s Hospital',
    'MSC1': 'Medical Science, Building I', #FIX
    'MSC2': 'Medical Science, Building II', #FIX
    'MSRB3': 'Medical Science Research, Building III', #FIX
    'NAME': 'Naval Architecture and Marine Engineering Building',
    'NCRB': 'North Campus Recreation Building',
    'NCRC': 'North Campus Research Complex',
    'NIB': '300 North Ingalls Building',
    '400NI': '400 North Ingalls Building',
    'NORTHVILLEPH': 'Northville State Hospital', #should this be the pychiatric hospital??
    'NQ': 'North Quad',
    'NS': 'Edward Henry Kraus Natural Science Building',
    'OBL': 'Observatory Lodge, 1402 Washington Heights',
    'PALM': 'Palmer Commons',
    'PHOENIXLAB': 'Phoenix Memorial Laboratory',
    'PIER': 'Pierpont Commons',
    'POWER CTR': 'Power Center for Performing Arts',
    'RACK': 'Horace H. Rackham, School of Graduate Studies',
    'RAND': 'Randall Laboratory',
    'R-BUS': 'Ross School of Business Building',
    'REVELLI': 'William D. Revelli Hall', #FIX
    'ROSS AC': 'Stephen M. Ross Academic Center',
    'RUTHVEN': 'A. G. Ruthven Museums Building',
    'SCHEM': 'Glenn E. Schembechler Hall', #FIX
    'SEB': 'School of Education Building',
    'SHAPIRO': 'Shapiro Undergraduate Library',
    'SM': 'Earl V. Moore Building, School of Music',
    'SNB': 'School of Nursing Building',
    'SNRE': 'Dana Samuel Trask Building (School of Natural Resources and Environment)', #FIX
    'SPH1': 'Henry Vaughan Building', #may need fixing
    'SPH2': 'Thomas Francis, Jr Building',
    'SRB': 'Space Research Building',
    'STB': '202 South Thayer Building',
    'STJOSEPH HOSP': 'St. Joseph Mercy Hospital',
    'STOCKWELL': 'Stockwell Hall',
    'STRNS': 'Sterns Building',
    'T&TB': 'Track and Tennis Building', #FIX
    'TAP': 'Tappan Hall',
    'TAUBL': 'Learning Resource Center, Taubman Medical Library',
    'TISCH': 'Tisch Hall',
    'UM HOSP': 'University Hospital Medical Campus',
    'UMMA': 'University of Michigan Museum of Art (Alumni Memorial Hall)',
    'UNION': 'Michigan Union',
    'USB': 'Undergraduate Science Building',
    'UTOWER': 'University Towers, 1225 S. University',
    'VETERANSHOSP': 'Veterans Administration Hospital',
    'WASHCTY HD': 'Washtenaw County Health Department', #FIX
    'W-BUS': 'Wyly Hall',
    'WDC': 'Charles R. Walgreen, Jr. Drama Center', #FIX: 1226 Murfin AVE
    'WEILL': 'Joan and Sanford Weill Hall', #FIX
    'WEIS': 'Weiser Hall',
    'WH': 'West Hall',
    'WOMEN\'S HOSP': 'Women\'s Hospital',
    'WQ': 'West Quad',
    #Public policy annex, 1015 E Huron wrong
}
    # need to iterate through all pairs in our large dict and make sure they work

    return render_template('test.html', **data)
