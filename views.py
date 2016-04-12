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
    data['current_term'] = term_code
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
    data['courses'] = get_catalog_numbers(term_code, school_code, subject_code) 
    data['course_sections'] = get_sections(term_code, school_code, 
                                    subject_code, catalog_number)
    data['section_meetings'] = get_meetings(term_code, school_code, subject_code,
                                    catalog_number, section_number)
    data['section_details'] = get_section_details(term_code, school_code, 
                                    subject_code, catalog_number, section_number)
    data['building_names'] = 

# building abbreviations from the office of the registrar - make into a dict
'''
A&AB Art & Architecture Building North Campus
AH  Angell Hall Central Campus
AL  Walter E. Lay Automotive Lab    North Campus
ALH Alice Lloyd Hall    The Hill Area
ANNEX   Public Policy Annex, 1015 E. Huron  Central Campus
ARGUS2  Argus Building II, Television Center, 408 S. Fourth Street  Ann Arbor, Off Campus
ARGUS3  Argus Building III, 416 S. Fourth Street    Ann Arbor, Off Campus
ARR Location to be Arranged Contact Dept or Instructor
BAM HALL    Blanch Anderson Moore Hall, School of Music North Campus
BELL POOL   Margaret Bell Pool, Central Campus Recreation Building  The Hill Area
BEYST   Bob and Betty Beyster Building (formerly CSE)   North Campus
BIOL STAT   Biological Station  Pellston, Michigan
BMT Burton Memorial Tower   Central Campus
BOT GARD    Matthaei Botanical Gardens, Dixboro Road    Ann Arbor, Off Campus
BSRB    Biomedical Science Research Building    Medical Campus
BURS    Bursley Hall    North Campus
BUS Business Administration Central Campus
CAMP DAVIS  Camp Davis  Jackson Hole, Wyoming
CCL Clarence Cook Little Building   Central Campus
CCRB    Central Campus Recreation Building  The Hill Area
CHEM    Chemistry Building  Central Campus
CHRYS   Chrysler Center North Campus
COMM PARK   Commerce Park   Dearborn, Michigan
COOL    Cooley Building North Campus
COUZENS Couzens Hall    The Hill Area
CPH Children's Psychiatric Hospital Medical Campus
CRISLER Crisler Arena   South Campus
CCSB    Campus Safety Services Building, 1239 Kipke Dr. South Campus
DANA    Dana Building (School of Natural Resources & Environment)   Central Campus
DANCE   Dance Building, 1310 N University Court The Hill Area
DC  Duderstadt Center   North Campus
DENN    David M. Dennison Building (to be renamed Weiser Hall)  Central Campus
DENT    Dental Building Central Campus
DOW Dow Engineering Building    North Campus
E-BUS   Executive Education Central Campus
EECS    Electrical Engineering and Computer Science Building    North Campus
EH  East Hall   Central Campus
EQ  East Quadrangle Central Campus
ERB1    Engineering Research Building 1 North Campus
ERB2    Engineering Research Building 2 North Campus
EWRE    Environmental & Water Resources Engineering Building    North Campus
FA CAMP Fresh Air Camp, Pinckney    Pinckney, Michigan
FORD LIB    Ford Library    North Campus
FXB Francois-Xavier Bagnoud Building    North Campus
GFL Gorguze Family Laboratory (formerly EPB)    North Campus
GGBL    G. G. Brown Laboratory  North Campus
GLIBN   Harlan Hatcher Graduate Library, North  Central Campus
HH  Haven Hall  Central Campus
HUTCH   Hutchins Hall   Central Campus
IM POOL Intramural Building South Campus
IOE Industrial and Operations Engineering Building  North Campus
ISR Institute for Social Research   Central Campus
K-BUS   Kresge Library  Central Campus
KEC Kellogg Eye Center  Medical Campus
KEENE THTR EQ   Keene Theater, Residential College, East Quadrangle Central Campus
KELSEY  Kelsey Museum of Archaeology    Central Campus
KHRI    Kresge Hearing Research Institute   Medical Campus
LANE    Lane Hall   Central Campus
LBME    Lurie Biomedical Engineering Building   North Campus
LEAG    Michigan League Central Campus
LEC Lurie Engineering Center    North Campus
LLIB    Law Library Central Campus
LORCH   Lorch Hall  Central Campus
LSA Literature, Science, and the Arts Building  Central Campus
LSI Life Sciences Institute Central Campus
LSSH    Law School South Hall   Central Campus
MARKLEY Mary Markley Hall   The Hill Area
MAX KADE    Max Kade House, 627 Oxford Street   Ann Arbor, Off Campus
MH  Mason Hall  Central Campus
MHRI    Mental Health Research Institute    Medical Campus
MLB Modern Languages Building   Central Campus
MONREOCTY HD    Monroe County Health Department Monroe, Michigan
MOSHER  Mosher Jordan Hall  The Hill Area
MOTT    C. S. Mott Children's Hospital  Medical Campus
MSC1    Medical Science, Building I Medical Campus
MSC2    Medical Science, Building II    Medical Campus
MSRB3   Medical Science Research, Building III  Medical Campus
NAME    Naval Architecture and Marine Engineering Building  North Campus
NCRB    North Campus Recreation Building    North Campus
NCRC    North Campus Research Complex   North Campus
NIB 300 North Ingalls Building  Medical Campus
400NI   400 North Ingalls Building (old School of Nursing Building) Medical Campus
NORTHVILLEPH    Northville State Hospital   Northville, Michigan
NQ  North Quad  Central Campus
NS  Edward Henry Kraus Natural Science Building Central Campus
OBL Observatory Lodge, 1402 Washington Heights  The Hill Area
PALM    Palmer Commons  Central Campus
PHOENIXLAB  Phoenix Memorial Laboratory North Campus
PIER    Pierpont Commons    North Campus
POWER CTR   Power Center for the Performing Arts    Central Campus
RACK    Horace H. Rackham, School of Graduate Studies   Central Campus
RAND    Randall Laboratory  Central Campus
R-BUS   Ross School of Business Building    Central Campus
REVELLI William D. Revelli Hall South Campus
ROSS AC Stephen M. Ross Academic Center South Campus
RUTHVEN A. G. Ruthven Museums Building (Natural History Museum) Central Campus
SCHEM   Glenn E. Schembechler Hall  South Campus
SEB School of Education Building    Central Campus
SHAPIRO Shapiro Undergraduate Library   Central Campus
SM  Earl V. Moore Building, School of Music North Campus
SNB School of Nursing Building  Medical Campus
SPH1    Henry Vaughan Building, School of Public Health I   The Hill Area
SPH2    Thomas Francis, Jr Building, School of Public Health II The Hill Area
SRB Space Research Building North Campus
SSWB    School of Social Work Building  Central Campus
STAMPS  Stamps Auditorium   North Campus
STB 202 South Thayer Building   Central Campus
STJOSEPH HOSP   St. Joseph Mercy Hospital   Ann Arbor, Off Campus
STOCKWELL   Stockwell Hall  The Hill Area
STRNS   Sterns Building North Campus
T&TB    Track & Tennis Building Ann Arbor, Off Campus
TAP Tappan Hall Central Campus
TAUBL   Learning Resource Center, Taubman Medical Library   Medical Campus
TISCH   Tisch Hall  Central Campus
UM HOSP University Hospital Medical Campus
UMMA    University of Michigan Museum of Art (Alumni Memorial Hall) Central Campus
UNION   Michigan Union  Central Campus
USB Undergraduate Science Building  Central Campus
UTOWER  University Towers, 1225 S. University   Central Campus
VETERANSHOSP    Veterans Administration Hospital    Ann Arbor, Off Campus
WASHCTY HD  Washtenaw County Health Department  Ann Arbor, Off Campus
W-BUS   Wyly Hall   Central Campus
WDC Charles R. Walgreen, Jr. Drama Center   North Campus
WEILL   Joan and Sanford Weill Hall Central Campus
WEIS    Weiser Hall (formerly Dennsion Building)    Central Campus
WH  West Hall   Central Campus
WOMEN'S HOSP    Women's Hospital    Medical Campus
WQ  West Quad   Central Campus
'''

locations = {
    
    'EH': 'East Hall',
    'EQ': 'East Quadrangle',
    'ERB1': 'Engineering Research Building 1',
    'ERB2': 'Engineering Research Building 2',
    'EWRE': 'Environmental & Water Resources Engineering Building',
    'FA CAMP': 'Fresh Air Camp, Pinckney',
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
    'SPH1': 'Henry Vaughan Building',
    'SPH2': 'Thomas Francis, Jr Building',
    'SRB': 'Space Research Building',
    'STB': '202 South Thayer Building',
    'STJOSEPH HOSP': 'St. Joseph Mercy Hospital',
    'STOCKWELL': 'Stockwell Hall',
    'STRNS': 'Sterns Building',
    'T&TB': 'Track & Tennis Building',
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

    #if doesn't work, use an empty data

    return render_template('about-us.html', **data)  
