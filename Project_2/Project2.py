## SI 206 W17 - Project 2

## COMMENT HERE WITH:
## Your name: Kyle Essenmacher
## Anyone you worked with on this project: Aaron Cheng, Michele Gee, Priscilla Nunez

## Below we have provided import statements, comments to separate out the
#parts of the project, instructions/hints/examples, and at the end, TESTS.

###########

## Import statements
import unittest
import requests
import re
from bs4 import BeautifulSoup


## Part 1 -- Define your find_urls function here.
## INPUT: any string
## RETURN VALUE: a list of strings that represents all of the URLs in the input string


## For example:
## find_urls("http://www.google.com is a great site") should return ["http://www.google.com"]
## find_urls("I love looking at websites like http://etsy.com and http://instagram.com and stuff") should return ["http://etsy.com","http://instagram.com"]
## find_urls("the internet is awesome #worldwideweb") should return [], empty list

def find_urls(s):
    url = re.findall('http\S*\.[a-z]+\S', s)
    return url

'''
The code above: 
1) finding all of the instances "http" shows up.
2) then it is taking out any white spaces with the \S*
3) next it is finding any character that is a-z
4) at the end it gives an output of the url
'''


## PART 2  - Define a function grab_headlines.
## INPUT: N/A. No input.
## Grab the headlines from the "Most Read" section of
## http://www.michigandaily.com/section/opinion

def grab_headlines():
    #Opening from opinion.html
    # f = open('opinion.html', 'r')
    # file = f.read()
    # f.close()

    #Opening from Michigan Daily
    r = requests.get('http://www.michigandaily.com/section/opinion')
    soup = BeautifulSoup(r.text, 'html.parser')
    most_read = []
    s = ""

    for most in soup.find_all(class_ = 'view view-most-read view-id-most_read view-display-id-panel_pane_1 view-dom-id-99658157999dd0ac5aa62c2b284dd266'):
        s = most.text.strip()
        most_read = s.split("\n")

    return most_read

'''
The code above is parsing through the Michigan Daily using the html.parser 
plugin I installed via pip install. It is going through the most read items 
on the site.
'''

## PART 3 (a) Define a function called get_umsi_data.  It should create a dictionary
## saved in a variable umsi_titles whose keys are UMSI people's names, and whose
## associated values are those people's titles, e.g. "PhD student" or "Associate
## Professor of Information"...
## Start with this page: https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All
## End with this page: https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All&page=12
## INPUT: N/A. No input.
## OUTPUT: Return umsi_titles
## Reminder: you'll need to use the special header for a request to the UMSI site, like so:
## requests.get(base_url, headers={'User-Agent': 'SI_CLASS'})

def get_umsi_data():
    umsi_titles = {}
    base_url = "https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All"
    r = requests.get(base_url, headers = {'User-Agent': 'SI_CLASS'})
    soup = BeautifulSoup(r.text, 'lxml')

    for i in range(13):
        if i == 0:
            base_url = 'https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All'
        else:
            base_url = 'https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All&page={}'.format(str(i))
        r = requests.get(base_url, headers = {'User-Agent': 'SI_CLASS'})
        soup = BeautifulSoup(r.text, 'lxml')
        field_name = soup.find_all('div', {'class': 'field-item even', 'property': 'dc:title'})
        field_position = soup.find_all('div', {'class': 'field field-name-field-person-titles field-type-text field-label-hidden'})
        for field_item in range(len(field_name)):
            umsi_titles[field_name[field_item].text] = field_position[field_item].text

    return umsi_titles

'''
The code above is going through the UMSI website directory using the BS4 plugin. 
It is finding the class, which is their titles and printing them in return. 
'''

## PART 3 (b) Define a function called num_students.
## INPUT: The dictionary from get_umsi_data().
## OUTPUT: Return number of PhD students in the data.  (Don't forget, I may change the input data)
def num_students(data):
    phd_students = 0

    for key in data:
        if data[key] == 'PhD student':
            phd_students += 1

    return phd_students

'''
The code above is going through the data to try and find "PHD Students" in the data set. If it sees the key "PhD student" in the key value pair it will add them to a counter and count all 
of the PhD students in the data. 

At the end of the code it will return the number of PhD students found. 
'''
########### TESTS; DO NOT CHANGE ANY CODE BELOW THIS LINE! ###########
def test(got, expected, pts):
    score = 0;
    if got == expected:
        score = pts
        print(" OK ",end=" ")
    else:
        print (" XX ", end=" ")
    print("Got: ",got, "Expected: ",expected)

    return score


def main():
    total = 0
    print()
    print ('Task 1: Find URLS')
    total += test(find_urls("http://www.google.com is a great site"),["http://www.google.com"],10)
    total += test(find_urls("I love looking at websites like http://etsy.com and http://instagram.com and lol.com and stuff"),["http://etsy.com","http://instagram.com"],10)
    total += test(find_urls("I love looking at websites like http://etsy and http://instagram.com and https://www.bbc.co.uk and stuff"),["http://instagram.com","https://www.bbc.co.uk"],10)
    total += test(find_urls("the internet is awesome #worldwideweb"),[],10)
    total += test(find_urls("http://.c"),[],10)

    print('Task 2: Michigan Daily')
    total += test(grab_headlines(),['Students attempt to shut down speech by controversial social scientist Charles Murray ', 'Orion Sang: Michigan should see what it has with Peters', "Protesters grapple with Charles Murray's appearance on campus", "'Lil Pump' delivers hype despite a lack of substance", "'Jane the Virgin' becomes Adam the Virgo in season 4 shift"] ,50)

    data = get_umsi_data()
    total += test(data, {'Mohamed Abbadi': 'PhD student', 'Mark Ackerman': 'George Herbert Mead Collegiate Professor of Human-Computer Interaction, Professor of Information, School of Information, Professor of Electrical Engineering and Computer Science, College of Engineering and Professor of Learning Health Sciences, Medical Sc', 'Eytan Adar': 'Associate Professor of Electrical Engineering and Computer Science, College of Engineering and Associate Professor of Information, School of Information', 'Julia Adler-Milstein': 'Adjunct Associate Professor of Information and Research Investigator, School of Information', 'Wei Ai': 'PhD student', 'Rasha Alahmad': 'PhD student', 'Tawfiq Ammari': 'PhD student', 'Komal Anand': 'Design, Innovation, and Engaged Learning Program Manager', 'Marsha Antal': 'School Registrar', 'Deborah Apsley': 'Director of Human Resources and Support Services', 'Daniel Atkins III': 'Professor Emeritus of Information, School of Information and Professor Emeritus of Electrical Engineering and Computer Science, College of Engineering', 'Seyram Avle': 'Research Investigator, Information and Research Fellow, School of Information', 'Todd Ayotte': 'Director of Finance', 'Alicia Baker': 'Administrative Assistant', 'Reginald Beasley': 'Admissions and Student Affairs Assistant', 'Vadim Besprozvany': 'Lecturer III in Information, School of Information', 'Lindsay Blackwell': 'PhD student', 'Francis Blouin Jr': 'Professor of Information, School of Information and Professor of History, College of Literature, Science, and the Arts', 'Walt Borland': 'Adjunct Clinical Associate Professor of Information, School of Information', 'Lia Bozarth': 'PhD student', 'Leah Brand': 'Project Manager', 'Stephanie Brenton': 'Intermittent Lecturer in Information, School of Information', 'Robin Brewer': 'Assistant Professor/Postdoctoral/Presidential Fellow, School of Information', 'Christopher Brooks': 'Research Assistant Professor, School of Information', 'Sophia Brueckner': 'Assistant Professor of Art and Design, Penny W Stamps School of Art and Design and Assistant Professor of Information, School of Information', 'Ceren Budak': 'Assistant Professor of Information, School of Information and Assistant Professor of Electrical Engineering and Computer Science, College of Engineering', 'Lorraine Buis': 'Assistant Professor of Family Medicine, Medical School and Assistant Professor of Information, School of Information', 'Glenda Bullock': 'Associate Director of Communications', 'Ryan Burton': 'PhD student', 'Ayse Buyuktur': 'Research Area Specialist, School of Information', 'Stacy Callahan': 'Financial Specialist Senior', 'Dan Cameron': 'Global Engagement Coordinator', 'Nick Campbell': 'Assistant Director of Development', 'Samuel Carton': 'PhD student', 'Kayla Carucci': 'PhD student', 'Melissa Chalmers': 'PhD student', 'Priyank Chandra': 'PhD student', 'Daphne Chang': 'PhD student', 'Yan Chen': 'PhD student', 'Jacques Chestnut': ' ', 'Padma Chirumamilla': 'PhD student', 'Heeryung Choi': 'PhD student', 'Amanda Ciacelli': 'Research and HR Administrative Assistant', 'Jaclyn Cohen': 'Lecturer III in Information, School of Information', 'Alain Cohn': 'Assistant Professor of Information, School of Information', 'Kevyn Collins-Thompson': 'Associate Professor of Information, School of Information and Associate Professor of Electrical Engineering and Computer Science, College of Engineering', 'Paul Conway': 'Associate Professor of Information, School of Information', 'Paul Courant': 'Harold T Shapiro Collegiate Professor of Public Policy, Arthur F Thurnau Professor, Senior Counselor to the Provost, Office of the Provost and Executive Vice President for Academic Affairs, Presidential Bicentennial Professor, Professor of Public Policy, ', 'Andrea Daly': 'Associate Director of Development and Alumni Relations', 'Shevon Desai': 'Senior Associate Librarian, Graduate Library, University Library', 'Tawanna Dillahunt': 'Assistant Professor of Information, School of Information and Assistant Professor of Electrical Engineering and Computer Science, College of Engineering', 'Nia Dowell': 'Research Investigator, Information and Research Fellow, School of Information', 'James Duderstadt': 'President Emeritus and University Professor of Science and Engineering', 'Katie Dunn': 'Assistant Director of Career Development and Adjunct Lecturer in Information, School of Information', 'Joan Durrance': 'Professor Emerita of Information, School of Information', 'Paul Edwards': 'Professor of Information, School of Information and Professor of History, College of Literature, Science, and the Arts', 'Laura Elgas': 'Director of Admissions and Student Affairs', 'Nicole Ellison': 'Professor of Information, School of Information', 'Rebecca Epstein': 'Executive Secretary', 'Luis Escareno': 'Development and Alumni Relations Generalist', 'Veronica Falandino': 'Associate Director for Admissions and Student Affairs', 'Thomas Finholt': 'Dean and Professor of Information, School of Information', 'Barry Fishman': 'Arthur F Thurnau Professor, Professor of Education, School of Education and Professor of Information, School of Information', 'Kanda Fletcher': 'Administrative Assistant Senior', 'Allen Flynn': 'PhD student', 'Kathleen Folger': 'Librarian, Library Collections, University Library', 'Kristin Fontichiaro': 'Clinical Associate Professor of  Information, School of Information', 'Rebecca Frank': 'PhD student', 'Charles Friedman': 'Josiah Macy, Jr Professor of Medical Education, Chair, Department of Learning Health Sciences, Professor of Learning Health Sciences, Medical School, Professor of Information, School of Information and Professor of Health Management and Policy, School of ', 'Carolyn Frost': 'Professor Emerita of Information, School of Information', 'George Furnas': 'Professor of Information, School of Information, Professor of Electrical Engineering and Computer Science, College of Engineering and Prof of Psychology, College of Literature, Science and the Arts', 'Patricia Garcia': 'Assistant Professor of Information, School of Information', 'Eric Gilbert': 'John Derby Evans Endowed Professor of Information and Associate Professor of Information, School of Information', 'Elena Godin': 'Lecturer IV in Information, School of Information', 'Iris Gomez-Lopez': 'Research Fellow, Information, School of Information', 'Carolyn Gregurich': 'HR Generalist', 'Tamy Guberek': 'PhD student', 'Hannah Haley': ' ', 'Brian Hall': 'PhD student', 'Alexandra Haller': ' ', 'David Hanauer': 'Associate Professor of  Pediatrics and Communicable Diseases, Medical School and Clinical Associate Professor of Information, School of Information', 'Edward Happ': 'Lecturer IV in Information and Research Investigator, School of Information', 'Jean Hardy': 'PhD student', 'Carl Haynes': 'PhD student', 'Shiqing (Licia) He': 'PhD student', 'Margaret Hedstrom': 'Robert M Warner Collegiate Professor of Information, Professor of Information, School of Information and Faculty Associate, Institute for Social Research', 'Libby Hemphill': 'Associate Professor of Information, School of Information and Research Associate Professor, Inter-University Consortium for Political and Social Research, Institute for Social Research', 'Michael Hess': 'Solution Architect Lead and Adjunct Lecturer in Information, Sch of Information, Director of Infrastructure ActiveStep, App Programmer/Analyst Ld, Family Medicine, Medical School', 'David Hessler': 'Professor Emeritus of Information, School of Information', 'James Hilton': 'Arthur F Thurnau Professor, Vice Provost for Academic Innovation, Office of the Provost and Executive Vice President for Academic Affairs, Dean of Libraries, University Library, Professor of Information, School of Information and Faculty Associate, Resear', 'Erik Hofer': 'Chief Information Officer and Clinical Assistant Professor of Information, School of Information', 'Lija Hogan': 'Intermittent Lecturer in Information, School of Information', 'Maurita Holland': 'Associate Professor Emerita of Information, School of Information', 'Caitlin Holman': 'PhD student', 'Evan Hoye': ' ', 'Joey Hsiao': 'PhD student', 'Chuan-Che Huang': 'PhD student', 'Julie Hui': 'Research Fellow, School of Information', 'Graham Hukill': 'Intermittent Lecturer in Information, School of Information', 'Pei-Yao Hung': 'PhD student', 'Linh Huynh': 'Academic Advisor', 'Bradley Iott': 'PhD student', 'Kelly Iott': 'Facilities Coordinator', 'Sheryl James': 'Public Relations Specialist', 'Grace YoungJoo Jeon': 'Research Fellow, Information, School of Information', 'Craig Johnson': 'Web Software Developer', 'Lynn Johnson': 'Professor of Dentistry, Department of Periodontics and Oral Medicine, Associate Dean for Faculty Affairs and Institutional Effectiveness, School of Dentistry and Clinical Professor of Information, School of Information', 'Ju Yeon Jung': 'PhD student', 'David Jurgens': 'Assistant Professor of Information, School of Information', 'Vaishnav Kameswaran': 'PhD student', 'Tsuyoshi Kano': 'PhD student', 'Harmanpreet Kaur': 'PhD student', 'Matthew Kay': 'Assistant Professor of Information, School of Information and Assistant Professor of Electrical Engineering and Computer Science, College of Engineering', 'Elizabeth Kaziunas': 'PhD student', 'Devon Keen': 'Assistant Director for Outreach and External Transfers', 'Sangmi Kim': 'PhD student', 'John Leslie King': 'William Warner Bishop Collegiate Professor of Information and Professor of Information, School of Information', 'Predrag Klasnja': 'Assistant Professor of Information, School of Information and Assistant Professor of Health Behavior and Health Education, School of Public Health', 'Daniel Klyn': 'Intermittent Lecturer I in Information, School of Information', 'Annie Knill': 'Assistant Director, Health Informatics Program', 'Kelly Kowatch': 'Director of Engaged Learning Programs and Adjunct Lecturer in Information, School of Information', 'Joanna Kroll': 'Director of Career Development and Adjunct Lecturer in Information, School of Information', 'Erin Krupka': 'Associate Professor of Information, School of Information', 'Carl Lagoze': 'Associate Professor of Information, School of Information', 'Clifford Lampe': 'Associate Professor of Information, School of Information', 'Walter Lasecki': 'Assistant Professor of Electrical Engineering and Computer Science, College of Engineering and Assistant Professor of Information, School of Information', 'Anna Lawrence': 'Digital Content Strategist', 'Katherine Lawrence': 'Research Area Specialist Lead and Research Investigator, School of Information', 'Judy Lawson': 'Assistant Dean for Diversity, Equity, and Inclusion', 'Claudia Leo': 'Programming and Media Coordinator', 'Margaret Levenstein': 'Adjunct Professor of Business Economics and Public Policy, Stephen M Ross School of Business, Research Professor, Survey Research Center, ISR Center Director, Institute for Social Research and Research Professor, School of Information', 'Melissa Levine': 'Librarian, Library Research - Copyright, University Library', 'Linfeng Li': 'PhD student', 'Yingzhi Liang': 'PhD student', 'cindy lin': 'PhD student', 'Silvia Lindtner': 'Assistant Professor of Information, School of Information and Assistant Professor of Art and Design, Penny W Stamps School of Art and Design', 'Jessica Litman': 'John F Nickoll Professor of Law, Professor of Law, Law School and Professor of Information, School of Information', 'John Lockard': 'Unix and IT Security Administrator', 'Jiaqi Ma': 'PhD student', 'Jeffrey MacKie-Mason': 'Dean Emeritus, Arthur W Burks Collegiate Professor Emeritus of Information and Computer Science, Professor Emeritus of Information, School of Information, Professor Emeritus of Economics, College of Literature, Science, and the Arts and Professor Emeritus', 'Danaja Maldeniya': 'PhD student', 'Megh Marathe': 'PhD student', 'Karen Markey': 'Professor of Information, School of Information', 'Robert Markum': 'PhD student', 'Allan Martell': 'PhD student', 'Yusuf Masatlioglu': 'Visiting Associate Professor of Economics, College of Literature, Science, and the Arts and Adjunct Associate Professor of Information, School of Information', 'Tonya McCarley': 'Intermittent Lecturer in Information, School of Information', 'Aprille McKay': 'Associate Archivist, Bentley Historical Library and Assistant Director, Bentley Historical Library and Adjunct Lecturer in Information, School of Information', 'Qiaozhu Mei': 'Associate Professor of Information, School of Information and Associate Professor of Electrical Engineering and Computer Science, College of Engineering', 'Abraham Mhaidli': 'PhD student', 'Markus Mobius': 'Adjunct Associate Professor of Information, School of Information', 'Liz Morris': 'PhD student', 'Carol Moser': 'PhD student', 'Nayiri Mullinix': 'Community Engagement and Exchange Coordinator', 'Sungjin Nam': 'PhD student', 'Michael Nebeling': 'Assistant Professor of Information, School of Information and Assistant Professor of Electrical Engineering and Computer Science, College of Engineering', 'Heather Newman': 'Director of Marketing and Communications', 'Mark Newman': 'Associate Professor of Information, School of Information and Associate Professor of Electrical Engineering and Computer Science, College of Engineering', 'Paige Nong': 'Program Manager and Research Coordinator', 'Adrienne Nwachukwu': 'Marketing Project Manager', "Rebecca O'Brien": 'Director of Research Administration', "Alaina O'Connor": 'Social Media Specialist', "Sile O'Modhrain": 'Associate Professor of Music, School of Music, Theatre & Dance and Associate Professor of Information, School of Information', 'Jo Angela Oehrli': 'Senior Associate Librarian, Learning and Teaching, University Library and Adjunct Lecturer in Curriculum Support, College of Literature, Science, and the Arts', 'Ihudiya Ogbonnaya-Ogburu': 'PhD student', 'Gary Olson': 'Professor Emeritus of Information, School of Information and Professor Emeritus of Psychology, College of Literature, Science, and the Arts', 'Judith Olson': 'Professor Emerita of Information, School of Information, Professor Emerita of Computation and Information Systems, Stephen M Ross School of Business and Professor Emerita of Psychology, College of Literature, Science, and the Arts', 'Steve Oney': 'Assistant Professor of Information, School of Information and Assistant Professor of Electrical Engineering and Computer Science, College of Engineering', 'Rebecca Pagels': 'Executive Director of Development and Alumni Relations', 'Joyojeet Pal': 'Assistant Professor of Information, School of Information', 'Sun Young Park': 'Assistant Professor of Art and Design, Penny W Stamps School of Art and Design and Assistant Professor of Information, School of Information', 'Dale Parry': 'Associate Director of Marketing', 'Gaurav Paruthi': 'PhD student', 'Desmond Patton': 'Assistant Professor of Social Work, School of Social Work and Assistant Professor of Information, School of Information', 'Hao Peng': 'PhD student', 'Katy Peters': 'Assistant Director for Undergraduate Programs', 'Chanda Phelan': 'PhD student', 'Casey Pierce': 'Assistant Professor of Information, School of Information', 'Edward Platt': 'PhD student', 'Martha Pollack': 'Professor of Information, School of Information, Professor of Electrical Engineering and Computer Science, College of Engineering and Provost and Executive Vice President for Academic Affairs, Office of the Provost and Executive Vice President for Academi', 'Corey Powell': 'Statistician Lead and Adjunct Lecturer in Information, School of Information', 'Christopher Quarles': 'PhD student', 'Dragomir Radev': 'Adjunct Professor of Information, School of Information and Adjunct Professor of Electrical Engineering and Computer Science, College of Engineering', 'Sonia Raheja': 'Marketing Assistant Associate', 'Shriti Raj': 'PhD student', 'Ashwin Rajadesingan': 'PhD student', 'Sarah Regan': 'Assistant Director, Master of Science in Information Program', 'Paul Resnick': 'Michael D Cohen Collegiate Professor of Information, Associate Dean for Research and Faculty Affairs, Professor of Information and Interim Director of Health Informatics, School of Information', 'Soo Young Rieh': 'Associate Professor of Information, School of Information', 'Lionel Robert': 'Associate Professor of Information, School of Information', 'Catherine Robinson': 'Research Process Coordinator', 'Daniel Romero': 'Assistant Professor of Information, School of Information, Assistant Professor of Electrical Engineering and Computer Science, College of Engineering and Assistant Professor of Complex Systems, College of Literature, Science, and the Arts', 'Victor Rosenberg': 'Associate Professor Emeritus of Information, School of Information', 'Tanya Rosenblat': 'Associate Professor of Information, School of Information and Associate Professor of Economics, College of Literature, Science, and the Arts', 'Nickie Rowsey': 'Accountant Senior', 'Jumanah Saadeh': 'Student Services Assistant', 'Perry Samson': 'Arthur F Thurnau Professor, Professor of Climate and Space Sciences and Engineering, College of Engineering and Professor of Information, School of Information', 'Nicholas Sands': 'Intermittent Lecturer in Information, School of Information', 'Christian Sandvig': 'Professor of Information, School of Information, Faculty Associate, Center for Political Studies, Institute for Social Research, Professor of Communication Studies, College of Literature, Science, and the Arts, and Professor of Art and Design, Penny W. St', 'Florian Schaub': 'Assistant Professor of Information, School of Information and Assistant Professor of Electrical Engineering and Computer Science, College of Engineering', 'Charles Severance': 'Clinical Associate Professor of Information, School of Information', 'Michael Shallcross': 'Associate Archivist and Assistant Director, Bentley Historical Library', 'Timothy Shannon': 'MHI Recruiting and Admissions Coordinator', 'Karandeep Singh': 'Assistant Professor of Learning Health Sciences, Assistant Professor of Internal Medicine, Medical School and Assistant Professor of Information, School of Information', 'Heidi Skrzypek': 'Assistant Director of Human Resources and Support Services', 'Thomas Slavens': 'Professor Emeritus of Information, School of Information', 'Barbara Smith': 'Senior Assistant to the Dean', 'Jeffrey Smith': 'Videographer', 'Elliot Soloway': 'Arthur F Thurnau Professor, Professor of Electrical Engineering and Computer Science, College of Engineering, Professor of Education, School of Education and Professor of Information, School of Information', 'Zhewei Song': 'PhD student', 'Maximilian Speicher': 'Research Fellow, School of Information', 'George Sprague': 'Academic Programs Coordinator', 'Scott Staelgraeve': 'Administrative Director', 'Todd Stuart': 'Events Manager', 'Hariharan Subramonyam': 'PhD student', 'Kyle Swanson': ' ', 'Allison Sweet': 'Graduate Programs Coordinator', 'Rohail Syed': 'PhD student', 'Alissa Talley-Pixley': 'Career Development and Engaged Learning Coordinator', 'Gregory Tasker': ' ', 'Marissa Taylor': 'Business Systems Analyst Intermediate/Associate', 'Stephanie Teasley': 'Research Professor, School of Information', 'D Scott TenBrink': 'Citizen Experience Design Community Development Liaison and Adjunct Lecturer in Information, School of Information', 'Chris Teplovs': 'Lecturer III in Information and Adjunct Lecturer in Information, School of Information', 'Andrea Thomer': 'Assistant Professor of Information, School of Information', 'Mark Thompson-Kolar': 'Intermittent Lecturer in Information, School of Information', 'Kentaro Toyama': 'W K Kellogg Professor of Community Information and Associate Professor of Information, School of Information', 'Penny Trieu': 'PhD student', 'Allison Tyler': 'PhD student', 'Douglas Van Houweling': 'Professor of Information, School of Information', 'Colleen Van Lent': 'Lecturer IV in Information, School of Information', 'Tiffany Veinot': 'Associate Professor of Information, School of Information and Associate Professor of Health Behavior and Health Education, School of Public Health', 'VG Vinod Vydiswaran': 'Assistant Professor of Learning Health Sciences, Medical School and Assistant Professor of Information, School of Information', 'David Wallace': 'Clinical Associate Professor of Information, School of Information', 'Lily Wang': ' ', 'Earnest Wheeler': 'PhD student', 'Brooke White': ' ', 'Elizabeth Whittaker': 'PhD student', 'Rachael Wiener': 'Assistant Director of Recruiting and Admissions, School of Information and Intermittent Lecturer in Social Work, School of Social Work', 'Michael Williams': 'Employer Relations Coordinator', 'Andy Wright': 'Systems Programmer Analyst', 'Elizabeth Yakel': 'Senior Associate Dean for Academic Affairs and Professor of Information, School of Information', 'Shiyan Yan': 'PhD student', 'Sarita Yardi Schoenebeck': 'Assistant Professor of Information, School of Information', 'Teng Ye': 'PhD student', 'Iman Yeckehzaare': 'PhD student', 'Jeremy York': 'PhD student', 'David Young': 'Multimedia Designer', 'T Charles Yun': 'Associate Director UMSI Computing', 'Shannon Zachary': 'Librarian, Library Collection, University Library and Adjunct Lecturer in Information, School of Information', 'Fangzhou Zhang': 'PhD student', 'Xinyan Zhao': 'PhD student', 'Yixin Zou': 'PhD student'} ,90)
    total += test(num_students(data), 67, 10)

    print(total)

if __name__ == '__main__':
    main()
