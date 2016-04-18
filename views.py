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
    'A&AB': 'Art and Architecture Building,Ann+Arbor+MI',
    'AH': 'Angell Hall,Ann+Arbor+MI',
    'AL': 'Walter E. Lay Automotive Lab,Ann+Arbor+MI',
    'ALH': 'Alice Lloyd Hall,Ann+Arbor+MI',
    'ANNEX': '1015 E. Huron,Ann+Arbor+MI', #fixed?
    'ARGUS2': '408 S. Fourth Street,Ann+Arbor+MI', #fixed?
    'ARGUS3': 'Argus Building III, 416 S. Fourth Street,Ann+Arbor+MI',
    'ARR': 'Location to be Arranged',
    'BAM HALL': 'Blanch Anderson Moore Hall, School of Music,Ann+Arbor+MI', #FIX
    'BELL POOL': 'Margaret Bell Pool, Central Campus Recreation Building,Ann+Arbor+MI', #FIX
    'BEYST': 'Bob and Betty Beyster Building,Ann+Arbor+MI',
    'BIOL STAT': 'Biological Station,Pellston+MI', #FIXED? one in pellston
    'BMT': 'Burton Memorial Tower,Ann+Arbor+MI',
    'BOT GARD': 'Matthaei Botanical Gardens, Dixboro Road,Ann+Arbor+MI',
    'BSRB': 'Biomedical Science Research Building,Ann+Arbor+MI',
    'BURS': 'Bursley Hall,Ann+Arbor+MI',
    'BUS': 'Business Administration,Ann+Arbor+MI',
    'CAMP DAVIS': 'Camp Davis, Jackson+Hole+Wyoming', #FIXED?
    'CCL': 'Clarence Cook Little Building,Ann+Arbor+MI',
    'CCRB': 'Central Campus Recreation Building,Ann+Arbor+MI',
    'CHEM': 'Chemistry Building,Ann+Arbor+MI', 
    'CHRYS': 'Chrysler Center,Ann+Arbor+MI', 
    'COMM PARK': '15041 S Commerce Dr.,Dearborn+MI+48120', #FIXED?: 15041 S Commerce Dr. Dearborn, MI 48120
    'COOL': 'Cooley Building,Ann+Arbor+MI',
    'COUZENS': 'Couzens Hall,Ann+Arbor+MI',
    'CPH': 'Children\'s Psychiatric Hospital,Ann+Arbor+MI',
    'CRISLER': 'Crisler Arena,Ann+Arbor+MI',
    'CCSB': 'Campus Safety Services Building, 1239 Kipke Dr.,Ann+Arbor+MI',
    'DANA': 'Dana Building (School of Natural Resources and Environment),Ann+Arbor+MI',
    'DANCE': 'Dance Building, 1310 N. University Court,Ann+Arbor+MI',
    'DC': 'Duderstadt Center,Ann+Arbor+MI',
    'DENN': 'David M. Dennison Building (Weiser Hall),Ann+Arbor+MI',
    'DENT': 'Dental Building,Ann+Arbor+MI',
    'DOW': 'Dow Engineering Building,Ann+Arbor+MI',
    'E-BUS': 'Executive Education,Ann+Arbor+MI',
    'EECS': 'Electrical Engineering and Computer Science Building,Ann+Arbor+MI',
    'EH': 'East Hall,Ann+Arbor+MI',
    'EQ': 'East Quadrangle,Ann+Arbor+MI',
    'ERB1': 'Engineering Research Building 1,Ann+Arbor+MI',
    'ERB2': 'Engineering Research Building 2,Ann+Arbor+MI',
    'EWRE': 'Environmental and Water Resources Engineering Building,Ann+Arbor+MI', 
    'FA CAMP': 'Fresh Air Camp,Pinckney+MI', #FIXED?
    'FORD LIB': 'Ford Library,Ann+Arbor+MI',
    'FXB': 'Francois-Xavier Bagnoud Building,Ann+Arbor+MI',
    'GFL': 'Gorguze Family Laboratory,Ann+Arbor+MI',
    'GGBL': 'G. G. Brown Laboratory,Ann+Arbor+MI',
    'GLIBN': 'Harlan Hatcher Graduate Library,Ann+Arbor+MI',
    'HH': 'Haven Hall,Ann+Arbor+MI',
    'HUTCH': 'Hutchins Hall,Ann+Arbor+MI',
    'IM POOL': 'Intramural Building,Ann+Arbor+MI',
    'IOE': 'Industrial and Operations Engineering Building,Ann+Arbor+MI',
    'ISR': 'Institute for Social Research,Ann+Arbor+MI',
    'K-BUS': 'Kresge Library,Ann+Arbor+MI',
    'KEC': 'Kellogg Eye Center,Ann+Arbor+MI',
    'KEENE THTR EQ': 'Keene Theater, Residential College, East Quadrangle,Ann+Arbor+MI',
    'KELSEY': 'Kelsey Museum of Archaeology,Ann+Arbor+MI',
    'KHRI': 'Kresge Hearing Research Institute,Ann+Arbor+MI', #FIX
    'LANE': 'Lane Hall,Ann+Arbor+MI',
    'LBME': 'Lurie Biomedical Engineering Building,Ann+Arbor+MI',
    'LEAG': 'Michigan League,Ann+Arbor+MI',
    'LEC': 'Lurie Engineering Center,Ann+Arbor+MI',
    'LLIB': 'Law Library,Ann+Arbor+MI', #FIX
    'LORCH': 'Lorch Hall,Ann+Arbor+MI',
    'LSA': 'Literature, Science, and the Arts Building,Ann+Arbor+MI',
    'LSI': 'Life Sciences Institute,Ann+Arbor+MI',
    'LSSH': 'Law School South Hall,Ann+Arbor+MI',
    'MARKLEY': 'Mary Markley Hall,Ann+Arbor+MI',
    'MAX KADE': 'Max Kade House, 627 Oxford Street,Ann+Arbor+MI', #FIX
    'MH': 'Mason Hall,Ann+Arbor+MI',
    'MHRI': 'Mental Health Research Institute,Ann+Arbor+MI',
    'MLB': 'Modern Languages Building,Ann+Arbor+MI',
    'MONROECTY HD': '2353+S+Custer+Rd,Monroe+MI+48161', #FIXED?: Monroe County Health Department, 2353 S custer Rd, Monroe< MI 48161
    'MOSHER': 'Mosher Jordan Hall,Ann+Arbor+MI',
    'MOTT': 'C.S. Mott Children\'s Hospital,Ann+Arbor+MI',
    'MSC1': 'Medical Science, Building I,Ann+Arbor+MI', #FIX
    'MSC2': 'Medical Science Building II,Ann+Arbor+MI', #FIX
    'MSRB3': 'Medical Science Research Building III,Ann+Arbor+MI', #FIX
    'NAME': 'Naval Architecture and Marine Engineering Building,Ann+Arbor+MI',
    'NCRB': 'North Campus Recreation Building,Ann+Arbor+MI',
    'NCRC': 'North Campus Research Complex,Ann+Arbor+MI',
    'NIB': '300 North Ingalls Building,Ann+Arbor+MI',
    '400NI': '400 North Ingalls Building,Ann+Arbor+MI',
    'NORTHVILLEPH': 'Northville State Hospital,Northville+MI', #does this work?
    'NQ': 'North Quad,Ann+Arbor+MI',
    'NS': 'Edward Henry Kraus Natural Science Building,Ann+Arbor+MI',
    'OBL': 'Observatory Lodge, 1402 Washington Heights,Ann+Arbor+MI',
    'PALM': 'Palmer Commons,Ann+Arbor+MI',
    'PHOENIXLAB': 'Phoenix Memorial Laboratory,Ann+Arbor+MI',
    'PIER': 'Pierpont Commons,Ann+Arbor+MI',
    'POWER CTR': 'Power Center for Performing Arts,Ann+Arbor+MI',
    'RACK': 'Horace H. Rackham, School of Graduate Studies,Ann+Arbor+MI',
    'RAND': 'Randall Laboratory,Ann+Arbor+MI',
    'R-BUS': 'Ross School of Business Building,Ann+Arbor+MI',
    'REVELLI': 'William D. Revelli Hall,Ann+Arbor+MI', #FIX
    'ROSS AC': 'Stephen M. Ross Academic Center,Ann+Arbor+MI',
    'RUTHVEN': 'A. G. Ruthven Museums Building,Ann+Arbor+MI',
    'SCHEM': 'Glenn E. Schembechler Hall,Ann+Arbor+MI', #FIX
    'SEB': 'School of Education Building,Ann+Arbor+MI',
    'SHAPIRO': 'Shapiro Undergraduate Library,Ann+Arbor+MI',
    'SM': 'Earl V. Moore Building, School of Music,Ann+Arbor+MI',
    'SNB': 'School of Nursing Building,Ann+Arbor+MI',
    'SPH1': 'Henry Vaughan Building,Ann+Arbor+MI', 
    'SPH2': 'Thomas Francis, Jr Building,Ann+Arbor+MI',
    'SRB': 'Space Research Building,Ann+Arbor+MI',
    'STB': '202 South Thayer Building,Ann+Arbor+MI',
    'STJOSEPH HOSP': 'St. Joseph Mercy Hospital,Ann+Arbor+MI',
    'STOCKWELL': 'Stockwell Hall,Ann+Arbor+MI',
    'STRNS': 'Sterns Building,Ann+Arbor+MI',
    'T&TB': 'Track and Tennis Building,Ann+Arbor+MI',
    'TAP': 'Tappan Hall,Ann+Arbor+MI',
    'TAUBL': 'Learning Resource Center, Taubman Medical Library,Ann+Arbor+MI',
    'TISCH': 'Tisch Hall,Ann+Arbor+MI',
    'UM HOSP': 'University Hospital Medical Campus,Ann+Arbor+MI',
    'UMMA': 'University of Michigan Museum of Art (Alumni Memorial Hall),Ann+Arbor+MI',
    'UNION': 'Michigan Union,Ann+Arbor+MI',
    'USB': 'Undergraduate Science Building,Ann+Arbor+MI',
    'UTOWER': 'University Towers, 1225 S. University,Ann+Arbor+MI',
    'VETERANSHOSP': 'Veterans Administration Hospital,Ann+Arbor+MI',
    'WASHCTY HD': 'Washtenaw County Health Department,Ann+Arbor+MI', #FIX
    'W-BUS': 'Wyly Hall,Ann+Arbor+MI',
    'WDC': '1226 Murfin Ave,Ann+Arbor+MI', #FIX: 1226 Murfin AVE, Charles R. Walgreen, Jr. Drama Center
    'WEILL': 'Joan and Sanford Weill Hall,Ann+Arbor+MI', #FIX
    'WEIS': 'Weiser Hall,Ann+Arbor+MI',
    'WH': 'West Hall,Ann+Arbor+MI',
    'WOMEN\'S HOSP': 'Women\'s Hospital,Ann+Arbor+MI',
    'WQ': 'West Quad,Ann+Arbor+MI',
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
    'A&AB': 'Art and Architecture Building,Ann+Arbor+MI',
    'AH': 'Angell Hall,Ann+Arbor+MI',
    'AL': 'Walter E. Lay Automotive Lab,Ann+Arbor+MI',
    'ALH': 'Alice Lloyd Hall,Ann+Arbor+MI',
    'ANNEX': '1015+E+Huron,Ann+Arbor+MI', #fixed?
    'ARGUS2': '408+S+4th+St,Ann+Arbor+MI', #fixed?
    'ARGUS3': 'Argus Building III, 416 S. Fourth Street,Ann+Arbor+MI',
    'ARR': 'Location to be Arranged',
    'BAM HALL': 'Blanch Anderson Moore Hall, School of Music,Ann+Arbor+MI', #FIX
    'BELL POOL': 'Margaret Bell Pool, Central Campus Recreation Building,Ann+Arbor+MI', #FIX
    'BEYST': 'Bob and Betty Beyster Building,Ann+Arbor+MI',
    'BIOL STAT': 'Biological Station,Pellston+MI', #FIXED? one in pellston
    'BMT': 'Burton Memorial Tower,Ann+Arbor+MI',
    'BOT GARD': 'Matthaei Botanical Gardens, Dixboro Road,Ann+Arbor+MI',
    'BSRB': 'Biomedical Science Research Building,Ann+Arbor+MI',
    'BURS': 'Bursley Hall,Ann+Arbor+MI',
    'BUS': 'Business Administration,Ann+Arbor+MI', # same building as kresge library in our maps - is that correct?
    'CAMP DAVIS': 'Camp Davis, Jackson+Hole+Wyoming', #FIXED?
    'CCL': 'Clarence Cook Little Building,Ann+Arbor+MI',
    'CCRB': 'Central Campus Recreation Building,Ann+Arbor+MI',
    'CHEM': 'Chemistry Building,Ann+Arbor+MI', # displays the wrong name (some lab inside chem building)
    'CHRYS': 'Chrysler Center,Ann+Arbor+MI', 
    'COMM PARK': '15041 S Commerce Dr.,Dearborn+MI+48120', #FIXED?: 15041 S Commerce Dr. Dearborn, MI 48120
    'COOL': 'Cooley Building,Ann+Arbor+MI',
    'COUZENS': 'Couzens Hall,Ann+Arbor+MI',
    'CPH': 'Children\'s Psychiatric Hospital,Ann+Arbor+MI',
    'CRISLER': 'Crisler Arena,Ann+Arbor+MI',
    'CCSB': 'Campus Safety Services Building, 1239 Kipke Dr.,Ann+Arbor+MI',
    'DANA': 'Dana Building (School of Natural Resources and Environment),Ann+Arbor+MI',
    'DANCE': 'Dance Building, 1310 N. University Court,Ann+Arbor+MI',
    'DC': 'Duderstadt Center,Ann+Arbor+MI',
    'DENN': 'David M. Dennison Building (Weiser Hall),Ann+Arbor+MI',
    'DENT': 'Dental Building,Ann+Arbor+MI',
    'DOW': 'Dow Engineering Building,Ann+Arbor+MI',
    'E-BUS': 'Executive Education,Ann+Arbor+MI', # what is this????
    'EECS': 'Electrical Engineering and Computer Science Building,Ann+Arbor+MI',
    'EH': 'East Hall,Ann+Arbor+MI',
    'EQ': 'East Quadrangle,Ann+Arbor+MI',
    'ERB1': 'Engineering Research Building 1,Ann+Arbor+MI',
    'ERB2': 'Engineering Research Building 2,Ann+Arbor+MI',
    'EWRE': 'Environmental and Water Resources Engineering Building,Ann+Arbor+MI', 
    'FA CAMP': 'Fresh Air Camp,Pinckney+MI', #FIXED?
    'FORD LIB': 'Ford Library,Ann+Arbor+MI',
    'FXB': 'Francois-Xavier Bagnoud Building,Ann+Arbor+MI',
    'GFL': 'Gorguze Family Laboratory,Ann+Arbor+MI',
    'GGBL': 'G. G. Brown Laboratory,Ann+Arbor+MI',
    'GLIBN': 'Harlan Hatcher Graduate Library,Ann+Arbor+MI',
    'HH': 'Haven Hall,Ann+Arbor+MI',
    'HUTCH': 'Hutchins Hall,Ann+Arbor+MI',
    'IM POOL': 'Intramural Building,Ann+Arbor+MI',
    'IOE': 'Industrial and Operations Engineering Building,Ann+Arbor+MI',
    'ISR': 'Institute for Social Research,Ann+Arbor+MI',
    'K-BUS': 'Kresge Library,Ann+Arbor+MI',
    'KEC': 'Kellogg Eye Center,Ann+Arbor+MI',
    'KEENE THTR EQ': 'Keene Theater, Residential College, East Quadrangle,Ann+Arbor+MI',
    'KELSEY': 'Kelsey Museum of Archaeology,Ann+Arbor+MI',
    'KHRI': 'Kresge Hearing Research Institute,Ann+Arbor+MI', #FIX
    'LANE': 'Lane Hall,Ann+Arbor+MI',
    'LBME': 'Lurie Biomedical Engineering Building,Ann+Arbor+MI',
    'LEAG': 'Michigan League,Ann+Arbor+MI',
    'LEC': 'Lurie Engineering Center,Ann+Arbor+MI',
    'LLIB': 'Law Library,Ann+Arbor+MI', #FIX
    'LORCH': 'Lorch Hall,Ann+Arbor+MI',
    'LSA': 'Literature, Science, and the Arts Building,Ann+Arbor+MI',
    'LSI': 'Life Sciences Institute,Ann+Arbor+MI',
    'LSSH': 'Law School South Hall,Ann+Arbor+MI',
    'MARKLEY': 'Mary Markley Hall,Ann+Arbor+MI',
    'MAX KADE': 'Max Kade House, 627 Oxford Street,Ann+Arbor+MI', #FIX
    'MH': 'Mason Hall,Ann+Arbor+MI',
    'MHRI': 'Mental Health Research Institute,Ann+Arbor+MI',
    'MLB': 'Modern Languages Building,Ann+Arbor+MI',
    'MONROECTY HD': '2353+S+Custer+Rd,Monroe+MI+48161', #FIXED?: Monroe County Health Department, 2353 S custer Rd, Monroe< MI 48161
    'MOSHER': 'Mosher Jordan Hall,Ann+Arbor+MI',
    'MOTT': 'C.S. Mott Children\'s Hospital,Ann+Arbor+MI',
    'MSC1': 'Medical Science, Building I,Ann+Arbor+MI', #FIX
    'MSC2': 'Medical Science Building II,Ann+Arbor+MI', #FIX
    'MSRB3': 'Medical Science Research Building III,Ann+Arbor+MI', #FIX
    'NAME': 'Naval Architecture and Marine Engineering Building,Ann+Arbor+MI',
    'NCRB': 'North Campus Recreation Building,Ann+Arbor+MI',
    'NCRC': 'North Campus Research Complex,Ann+Arbor+MI',
    'NIB': '300+North+Ingalls+Building,Ann+Arbor+MI',
    '400NI': '400+North+Ingalls+Building,Ann+Arbor+MI',
    'NORTHVILLEPH': 'Northville State Hospital,Northville+MI', #does this work?
    'NQ': 'North Quad,Ann+Arbor+MI',
    'NS': 'Edward Henry Kraus Natural Science Building,Ann+Arbor+MI',
    'OBL': 'Observatory Lodge, 1402 Washington Heights,Ann+Arbor+MI',
    'PALM': 'Palmer Commons,Ann+Arbor+MI',
    'PHOENIXLAB': 'Phoenix Memorial Laboratory,Ann+Arbor+MI',
    'PIER': 'Pierpont Commons,Ann+Arbor+MI',
    'POWER CTR': 'Power Center for Performing Arts,Ann+Arbor+MI',
    'RACK': 'Horace H. Rackham, School of Graduate Studies,Ann+Arbor+MI',
    'RAND': 'Randall Laboratory,Ann+Arbor+MI',
    'R-BUS': 'Ross School of Business Building,Ann+Arbor+MI',
    'REVELLI': 'William D. Revelli Hall,Ann+Arbor+MI', #FIX
    'ROSS AC': 'Stephen M. Ross Academic Center,Ann+Arbor+MI',
    'RUTHVEN': 'A. G. Ruthven Museums Building,Ann+Arbor+MI',
    'SCHEM': 'Glenn E. Schembechler Hall,Ann+Arbor+MI', #FIX
    'SEB': 'School of Education Building,Ann+Arbor+MI',
    'SHAPIRO': 'Shapiro Undergraduate Library,Ann+Arbor+MI',
    'SM': 'Earl V. Moore Building, School of Music,Ann+Arbor+MI',
    'SNB': 'School of Nursing Building,Ann+Arbor+MI',
    'SPH1': 'Henry Vaughan Building,Ann+Arbor+MI', 
    'SPH2': 'Thomas Francis, Jr Building,Ann+Arbor+MI',
    'SRB': 'Space Research Building,Ann+Arbor+MI',
    'STB': '202 South Thayer Building,Ann+Arbor+MI',
    'STJOSEPH HOSP': 'St. Joseph Mercy Hospital,Ann+Arbor+MI',
    'STOCKWELL': 'Stockwell Hall,Ann+Arbor+MI',
    'STRNS': 'Sterns Building,Ann+Arbor+MI',
    'T&TB': 'Track and Tennis Building,Ann+Arbor+MI',
    'TAP': 'Tappan Hall,Ann+Arbor+MI',
    'TAUBL': 'Learning Resource Center, Taubman Medical Library,Ann+Arbor+MI',
    'TISCH': 'Tisch Hall,Ann+Arbor+MI',
    'UM HOSP': 'University Hospital Medical Campus,Ann+Arbor+MI',
    'UMMA': 'University of Michigan Museum of Art (Alumni Memorial Hall),Ann+Arbor+MI',
    'UNION': 'Michigan Union,Ann+Arbor+MI',
    'USB': 'Undergraduate Science Building,Ann+Arbor+MI',
    'UTOWER': 'University Towers, 1225 S. University,Ann+Arbor+MI',
    'VETERANSHOSP': 'Veterans Administration Hospital,Ann+Arbor+MI',
    'WASHCTY HD': 'Washtenaw County Health Department,Ann+Arbor+MI', #FIX
    'W-BUS': 'Wyly Hall,Ann+Arbor+MI',
    'WDC': '1226 Murfin Ave,Ann+Arbor+MI', #FIX: 1226 Murfin AVE, Charles R. Walgreen, Jr. Drama Center
    'WEILL': 'Joan and Sanford Weill Hall,Ann+Arbor+MI', #FIX
    'WEIS': 'Weiser Hall,Ann+Arbor+MI',
    'WH': 'West Hall,Ann+Arbor+MI',
    'WOMEN\'S HOSP': 'Women\'s Hospital,Ann+Arbor+MI',
    'WQ': 'West Quad,Ann+Arbor+MI'
}
    # need to iterate through all pairs in our large dict and make sure they work

    return render_template('test.html', **data)
