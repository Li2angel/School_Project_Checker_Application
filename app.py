import sqlite3
from flask import Flask, render_template, request, redirect, session, url_for, flash, redirect, send_from_directory
from formsubmission import SchoolResulCheckerForm

app = Flask(__name__)
app.secret_key = "__privatekey__"

def __init__(self):
    # Database connection
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create user and project tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_title TEXT NOT NULL,
            student_name TEXT NOT NULL,
            registration_number TEXT NOT NULL,
            description TEXT,
            done BOOLEAN DEFAULT 0
        )
    ''')

    conn.commit()

#HOME PAGE
@app.route('/')
def home():
    return render_template('homepage.html')

#LOGIN PAGE
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        statement = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cursor.execute(statement)

        if not cursor.fetchone():
            return render_template('login.html')
        else:
            return render_template('projects.html', name = username)

    else:
        request.method == 'GET'
        return render_template('login.html')

#REGISTRATION PAGE
@app.route('/register', methods=['POST','GET'])
def register():
    registerForm = SchoolResulCheckerForm()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        if registerForm.validate == "False":
            flash("Please fill out this field")
            return render_template('register.html', form=registerForm)
        
        if(request.form['name'] != "" and request.form['password'] != ""):
            username = request.form['name']
            password = request.form['password']
            statement = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            cursor.execute(statement)
            data = cursor.fetchone()
            if data:
                return 'That username already exists!'
            else:
                if not data:
                    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",(username, password))
                    conn.commit()
                    conn.close()
                return render_template('login.html')
    elif request.method == 'GET':
        return render_template('register.html', form=registerForm)
    
#Adding Project
@app.route('/add_project', methods=['POST'])
def add_project():
    message = None
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        project_title = request.form['project_title']
        student_name = request.form['student_name']
        registration_number = request.form['registration_number']
        description = request.form['description']
        done = request.form.get('done', 0)  # Retrieve the checkbox value (1 if checked, 0 if not)
        
        #Check if Project Topic keywords exist in database
        cursor.execute("SELECT * FROM projects WHERE project_title=?", (project_title,))
        matching_projects = cursor.fetchall()
       
        if matching_projects:
            #message = f"Projects related to '{project_title}': {', '.join(project[0] for project in matching_projects)}"
            return render_template('projects.html', message=matching_projects, project_name=project_title)
        else:
            #Save the Project Details
            cursor.execute('''
                INSERT INTO projects (project_title, student_name, registration_number, description, done)
                VALUES (?, ?, ?, ?, ?)
            ''', (project_title, student_name, registration_number, description, done))
            conn.commit()  # Commit the changes to the database
            message = f"New project topic is saved."
    return  render_template('homepage.html', message=message, result=None, project_name=None)

#SEARCHING Projects
@app.route('/search_project', methods=['GET', 'POST'])
def search_project():
        user_keywords = request.form['project_title'].lower()
        similar_projects = check_project_exists(user_keywords)
        return render_template('homepage.html', result=similar_projects)

def check_project_exists(keywords):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    similar_projects = []
    # Fetch projects matching the keywords from the database
    cursor.execute("SELECT * FROM projects WHERE project_title LIKE ?", ('%{}%'.format(keywords),))
    similar_projects = [row for row in cursor.fetchall()]
    return similar_projects

if __name__ == '__main__':
    app.run(debug=True)
