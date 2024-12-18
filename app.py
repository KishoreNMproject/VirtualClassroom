from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os
import boto3
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = 'temporary_key'

# Database connection
# def get_db_connection():
#     return mysql.connector.connect(
#         host='vclassdb.cr22y8aic3s4.ap-south-1.rds.amazonaws.com',
#         user='admin',
#         password='admin9445520766',
#         database='students'
#     )

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
        
        # hashed_password = generate_password_hash(password, method='sha256')

        # Connect to the database and insert the user details
        # conn = get_db_connection()
        # cursor = conn.cursor()
        # cursor.execute('INSERT INTO users (fullname, email, username, password_hash) VALUES (%s, %s, %s, %s)',
        #                (fullname, email, username, hashed_password))
        # conn.commit()
        # cursor.close()
        # conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

# AWS S3 configuration
# s3 = boto3.client('s3', 
#                   aws_access_key_id='access_key', 
#                   aws_secret_access_key='secret_key',
#                   region_name='ap-south-1')
# BUCKET_NAME = 'awsprject'

@app.route('/admindashboard', methods=['GET'])
def admindashboard():
    return render_template('admindashboard.html')

@app.route('/upload', methods=['POST'])
def upload():
    course_title = request.form.get('courseTitle')
    file = request.files.get('file')

    # Validate file
    if file and file.filename.endswith('.pdf'):
        # Dummy flash message (no actual upload)
        flash(f"File '{file.filename}' uploaded successfully for course '{course_title}'!")
        return redirect(url_for('admindashboard'))
    else:
        flash('Only PDF files are allowed!')
        return redirect(url_for('admindashboard'))


# @app.route('/upload', methods=['POST'])
# def upload():
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(url_for('admindashboard'))
    
#     file = request.files['file']
#     course_name = request.form['courseTitle']

#     if file.filename == '':
#         flash('No selected file')
#         return redirect(url_for('admindashboard'))
    
#     if file and file.filename.endswith('.pdf'):
#         # Secure the filename
#         #filename = secure_filename(file.filename)
#         # Upload to S3
#         # s3.upload_fileobj(
#         #     file,
#         #     BUCKET_NAME,
#         #     filename,
#         #     ExtraArgs={"ContentType": "application/pdf"}
#         # )
#         # Save course info to database
#         # cur = mysql.connection.cursor()
#         # s3_url = f"https://{BUCKET_NAME}.s3.ap-south-1.amazonaws.com/{filename}"
#         # cur.execute("INSERT INTO courses (course_name, pdf_url) VALUES (%s, %s)", (course_name, s3_url))
#         # mysql.connection.commit()
#         # cur.close()
        
#         flash('Course uploaded successfully!')
#         return redirect(url_for('admindashboard'))
#     else:
#         alert('Invalid file type. Please upload a PDF.')
#         return redirect(url_for('admindashboard'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # conn = get_db_connection()
        # cursor = conn.cursor()
        # cursor.execute('SELECT password_hash FROM users WHERE username = %s', (username,))
        # result = cursor.fetchone()
        # cursor.close()
        # conn.close()

        if username and password:
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

    

# Dashboard Route (after login)
@app.route('/dashboard')
def dashboard():
    course_urls = [
        'https://drive.google.com/file/d/1H3hDaz2j0YpaAmBgJgnEVV0B3xjGP1-W/view?usp=sharing',
        'https://drive.google.com/file/d/1CaObWRHdNkP0xE-z3AAHUJqYRwq08AQP/view?usp=sharing'
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

@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')

if __name__ == '__main__':
    app.run(debug=True)
