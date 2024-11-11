from flask import Flask, request, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
<<<<<<< Updated upstream
app.secret_key = 'temporary_key'  # Replace with a secure key in production
=======
app.secret_key = 'temporary_key'  # Use a secret key for session management
>>>>>>> Stashed changes

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='your_db_user',
        password='your_db_password',
        database='your_db_name'
    )

<<<<<<< Updated upstream
# Home Route
@app.route('/')
def home():
    return render_template('home.html')
=======
# AWS S3 credentials (ensure these are set up correctly in your AWS IAM user)
s3 = boto3.client(
    's3',
    aws_access_key_id='YOUR_AWS_ACCESS_KEY',
    aws_secret_access_key='YOUR_AWS_SECRET_KEY',
    region_name='ap-south-1'  # Region where the bucket is located
)

BUCKET_NAME = 'awsprject'

# Admin Dashboard (to view and upload files)
@app.route('/admindashboard', methods=['GET', 'POST'])
def admindashboard():
    if 'logged_in' not in session:
        return redirect(url_for('admin_login'))  # Ensure the user is logged in
    
    files = list_uploaded_files()  # Get files from S3 bucket
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file and upload_file_to_s3(file, BUCKET_NAME):  # Upload to S3
            return redirect(url_for('admindashboard'))  # Refresh dashboard

    return render_template('admindashboard.html', files=files)

# Function to list files in the S3 bucket
def list_uploaded_files():
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    files = []
    if 'Contents' in response:
        for file in response['Contents']:
            file_info = {
                'name': file['Key'],
                'url': f'https://{BUCKET_NAME}.s3.amazonaws.com/{file["Key"]}'
            }
            files.append(file_info)
    return files

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

>>>>>>> Stashed changes

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash FROM users WHERE username = %s', (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result and check_password_hash(result[1], password):
            session['user_id'] = result[0]
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials', 401

    return render_template('login.html')

<<<<<<< Updated upstream
# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    course_urls = [
        'https://aws-project-virtualclassroom.s3.ap-south-1.amazonaws.com/python_code.pdf',
        'https://aws-project-virtualclassroom.s3.ap-south-1.amazonaws.com/PYTHON+PROGRAMMING+NOTES.pdf'
    ]
    return render_template('dashboard.html', course_urls=course_urls)

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (%s, %s)', (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')
=======

@app.route('/dashboard')
def dashboard():
    course_urls = list_uploaded_files()  # Fetch files from S3 for the student dashboard
    
    return render_template('dashboard.html', course_urls=course_urls)



# Home Route (Landing Page)
@app.route('/')
def home():
    return render_template('home.html')


# Admin Login Route
@app.route('/adminlogin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':  # When the form is submitted
        username = request.form['username']
        password = request.form['password']

        # Check if the credentials are correct
        if username == "admin1" and password == "1234":
            session['logged_in'] = True  # Set session variable indicating the user is logged in
            return redirect(url_for('admindashboard'))  # Redirect to the dashboard
        else:
            error_message = "Invalid username or password. Please try again."
            return render_template('adminlogin.html', error=error_message)  # Show error message

    # Handle GET request: Render the login page
    return render_template('adminlogin.html')


# Admin Dashboard Route (accessible only if logged in)
@app.route('/admindashboard')
def admindashboard():
    if 'logged_in' in session:  # Check if the user is logged in
        return render_template('admindashboard.html')  # Render the admin dashboard page
    else:
        return redirect(url_for('adminlogin'))  # If not logged in, redirect to the login page

>>>>>>> Stashed changes

# Logout Route
@app.route('/logout')
def logout():
<<<<<<< Updated upstream
    session.pop('user_id', None)
    return redirect(url_for('login'))
=======
    session.pop('logged_in', None)  # Remove 'logged_in' from the session to log the user out
    return redirect(url_for('admin_login'))  # Redirect to the admin login page

>>>>>>> Stashed changes

if __name__ == '__main__':
    app.run(debug=True)
