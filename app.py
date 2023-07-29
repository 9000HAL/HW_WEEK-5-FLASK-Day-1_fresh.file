from flask import Flask, request, render_template
import requests



app = Flask(__name__)




#--------ROUTES---------------------

@app.route("/")
def hello_world():
    return "<p>Hello, THIEVES-2023!</p>"



@app.route('/home')
def home():
    return '<h1>This is the home page</h1>'



@app.route('/user/<username>')
def username(username):
    # show the user profile for that user
    return f'Hello {username}!'



@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'




#HTTP methods:

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return '<h1>Logged In</h1>'
    else:
        return render_template('forms.html')




#########STUDENTS EXAMPLE

@app.route('/students')
def students():
    students_lst = ['Gabe', 'Will', 'Sean', 'Peace']
    return render_template('students.html', students_lst=students_lst)









########################### ERGAST EXAMPLE

@app.route('/ergast', methods=['GET', 'POST'])
def ergast():
    if request.method == 'POST':
        year = request.form.get('year')
        rnd = request.form.get('rnd')
        
        url = f'http://ergast.com/api/f1/{year}/{rnd}/driverStandings.json'
        response = requests.get(url)
        if response.ok:
            try:
                standings_data = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
                driver_data = get_driver_info(standings_data)
                return render_template('ergast.html', driver_data=driver_data)
            except IndexError:
                return 'That year or round does not exist!'
    return render_template('ergast.html')

#   REMOVED:                  return get_driver_info(standings_data)



# HELPER FUNCTION FORM DAY 4 WEEK 4 CLASS LECTURE BELOW:

def get_driver_info(data):
    new_driver_data = []
    for driver in data:
        driver_dict = {
            'full_name': f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}",
            'DOB': driver['Driver']['dateOfBirth'],
            'wins': driver['wins'],
            'team': driver['Constructors'][0]['name']
        }
        if len(new_driver_data) <=5:
            new_driver_data.append(driver_dict)
    return new_driver_data






########################### ERGAST EXAMPLE page renders no error but
"""  

@app.route('/ergast', methods=['GET', 'POST'])
def ergast():
    if request.method == 'POST':
        year = request.form.get('year')
        rnd = request.form.get('rnd')
        
        url = f'http://ergast.com/api/f1/{year}/{rnd}/driverStandings.json'
        response = requests.get(url)
        if response.ok:
            try:
                standings_data = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
                return get_driver_info(standings_data)
            except IndexError:
                return 'That year or round does not exist!'
    return render_template('ergast.html')

"""  
    
