from flask import Flask, request, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'temporary_key'

# Database connection new
def get_db_connection():
    return mysql.connector.connect(
        host='vclassdb.cr22y8aic3s4.ap-south-1.rds.amazonaws.com',
        user='admin',
        password='admin9445520766',
        database='students'
    )

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Collect user data from the form
        fullname = request.form['fullname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmpassword']
        
        # Check if passwords match
        if password != confirm_password:
            return 'Passwords do not match', 400
        
        hashed_password = generate_password_hash(password, method='sha256')

        # Connect to the database and insert the user details
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (fullname, email, username, password_hash) VALUES (%s, %s, %s, %s)',
                       (fullname, email, username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')



# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM users WHERE username = %s', (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result and check_password_hash(result[0], password):
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

# Dashboard Route (after login)
@app.route('/dashboard')
def dashboard():
    course_urls = [
        'https://aws-project-virtual-classroom.s3.us-east-1.amazonaws.com/python_code.pdf',
        'https://aws-project-virtual-classroom.s3.us-east-1.amazonaws.com/Python+Programming.pdf'
    ]
    
    return render_template('dashboard.html', course_urls=course_urls)

# Home Route (Landing Page)
@app.route('/')
def home():
    return render_template('home.html')
#cloud
@app.route('/')
def cloud():
    return redirect(url_for('cloud'))

# Logout
@app.route('/logout')
def logout():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
