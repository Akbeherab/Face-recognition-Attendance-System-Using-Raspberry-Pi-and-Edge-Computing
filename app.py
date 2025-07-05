from flask import Flask, render_template, request, redirect, url_for, send_file, Response, session, flash
import threading
import cv2
import face_recognition
import pickle
import pandas as pd
import os
from datetime import datetime, date
import time
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pdfkit
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['ATTENDANCE_TIME_LIMIT'] = '09:30'  # Time limit for being "on time"
app.config['ADMIN_USERNAME'] = 'admin'
app.config['ADMIN_PASSWORD'] = generate_password_hash('admin123')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    if user_id == app.config['ADMIN_USERNAME']:
        user = User()
        user.id = user_id
        return user
    return None

# Load encodings
try:
    with open("encodings.pkl", "rb") as f:
        data = pickle.load(f)
except FileNotFoundError:
    data = {"names": [], "encodings": []}

# Attendance tracking
attendance_log = {}
logged_names = set()
student_bios = {}

# Database simulation (in a real app, use a proper database)
students_db = {}
try:
    students_db = pd.read_excel("students.xlsx").to_dict(orient='records')
    for student in students_db:
        student_bios[student['name']] = student
except FileNotFoundError:
    pass

# Login required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != app.config['ADMIN_USERNAME']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Face recognition thread
def recognize_faces():
    global attendance_log, logged_names
    cap = cv2.VideoCapture(0)
    time.sleep(2)  # Warm-up camera

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)
        encs = face_recognition.face_encodings(rgb, boxes)

        for enc, box in zip(encs, boxes):
            matches = face_recognition.compare_faces(data["encodings"], enc)
            name = "Unknown"

            if True in matches:
                idx = matches.index(True)
                name = data["names"][idx]

                if name not in logged_names:
                    now = datetime.now()
                    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Check if on time or late
                    time_limit = datetime.strptime(f"{now.date()} {app.config['ATTENDANCE_TIME_LIMIT']}", "%Y-%m-%d %H:%M")
                    status = "On Time" if now <= time_limit else "Late"
                    
                    attendance_log[name] = {
                        'timestamp': timestamp,
                        'status': status,
                        'day': now.strftime("%A")
                    }
                    logged_names.add(name)
                    print(f"[INFO] Marked {name} as {status} at {timestamp}")

        time.sleep(1)  # reduce CPU load

# Video streaming generator
def gen_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Routes
@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    # Get today's attendance
    today = date.today().strftime("%Y-%m-%d")
    df = pd.DataFrame(columns=["Name", "Timestamp", "Status", "Day"])
    
    # Load attendance if exists
    if os.path.exists("attendance.xlsx"):
        df = pd.read_excel("attendance.xlsx")
        # Filter for today's records
        df = df[df['Timestamp'].apply(lambda x: str(x).startswith(today) if pd.notna(x) else False)]
    
    # Add real-time attendance
    for name, record in attendance_log.items():
        if record['timestamp'].startswith(today):
            df = pd.concat([df, pd.DataFrame([{
                "Name": name,
                "Timestamp": record['timestamp'],
                "Status": record['status'],
                "Day": record['day']
            }])], ignore_index=True)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['Name'], keep='last')
    
    # Add absent students
    all_names = set(data["names"])
    present_names = set(df["Name"])
    for name in all_names - present_names:
        df = pd.concat([df, pd.DataFrame([{
            "Name": name,
            "Timestamp": "-",
            "Status": "Absent",
            "Day": datetime.now().strftime("%A")
        }])], ignore_index=True)
    
    # Sort by status (Present first)
    df = df.sort_values(by=['Status'], ascending=False)
    
    return render_template("index.html", 
                         attendance=df.to_dict(orient="records"),
                         now=datetime.now(),
                         student_bios=student_bios)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == app.config['ADMIN_USERNAME'] and check_password_hash(app.config['ADMIN_PASSWORD'], password):
            user = User()
            user.id = username
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/download_excel')
@login_required
def download_excel():
    df = pd.DataFrame(columns=["Name", "Timestamp", "Status", "Day"])
    
    if os.path.exists("attendance.xlsx"):
        df = pd.read_excel("attendance.xlsx")
    
    # Add real-time attendance
    for name, record in attendance_log.items():
        df = pd.concat([df, pd.DataFrame([{
            "Name": name,
            "Timestamp": record['timestamp'],
            "Status": record['status'],
            "Day": record['day']
        }])], ignore_index=True)
    
    # Save to temporary file
    temp_file = "temp_attendance.xlsx"
    df.to_excel(temp_file, index=False)
    
    return send_file(temp_file, as_attachment=True, download_name=f"attendance_{datetime.now().strftime('%Y%m%d')}.xlsx")

@app.route('/download_pdf')
@login_required
def download_pdf():
    df = pd.DataFrame(columns=["Name", "Timestamp", "Status", "Day"])
    
    if os.path.exists("attendance.xlsx"):
        df = pd.read_excel("attendance.xlsx")
    
    # Add real-time attendance
    for name, record in attendance_log.items():
        df = pd.concat([df, pd.DataFrame([{
            "Name": name,
            "Timestamp": record['timestamp'],
            "Status": record['status'],
            "Day": record['day']
        }])], ignore_index=True)
    
    # Generate HTML
    html = render_template('pdf_template.html', 
                         attendance=df.to_dict(orient="records"),
                         now=datetime.now())
    
    # Convert to PDF
    pdf = pdfkit.from_string(html, False)
    
    return Response(pdf, mimetype="application/pdf", 
                  headers={"Content-Disposition": f"attachment;filename=attendance_{datetime.now().strftime('%Y%m%d')}.pdf"})

@app.route('/enroll', methods=['GET', 'POST'])
@admin_required
def enroll():
    if request.method == 'POST':
        name = request.form.get('name')
        roll_no = request.form.get('roll_no')
        department = request.form.get('department')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        # Handle file upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and allowed_file(file.filename):
                filename = f"{name}_{roll_no}.{file.filename.rsplit('.', 1)[1].lower()}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Add to student bios
                student_bios[name] = {
                    'name': name,
                    'roll_no': roll_no,
                    'department': department,
                    'email': email,
                    'phone': phone,
                    'photo': filename
                }
                
                # Update students database
                students_db.append(student_bios[name])
                pd.DataFrame(students_db).to_excel("students.xlsx", index=False)
                
                # Generate face encoding
                image = face_recognition.load_image_file(filepath)
                encodings = face_recognition.face_encodings(image)
                
                if encodings:
                    data["names"].append(name)
                    data["encodings"].append(encodings[0])
                    with open("encodings.pkl", "wb") as f:
                        pickle.dump(data, f)
                    
                    flash(f'Successfully enrolled {name}', 'success')
                else:
                    flash('No face detected in the image', 'error')
            else:
                flash('Invalid file format', 'error')
        else:
            flash('No file uploaded', 'error')
    
    return render_template('enroll.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    if request.method == 'POST':
        new_time_limit = request.form.get('time_limit')
        if new_time_limit:
            app.config['ATTENDANCE_TIME_LIMIT'] = new_time_limit
            flash('Time limit updated successfully', 'success')
    
    return render_template('settings.html', current_time_limit=app.config['ATTENDANCE_TIME_LIMIT'])

# Background tasks
def save_attendance_periodically():
    while True:
        if attendance_log:
            # Load existing data
            df = pd.DataFrame(columns=["Name", "Timestamp", "Status", "Day"])
            if os.path.exists("attendance.xlsx"):
                df = pd.read_excel("attendance.xlsx")
            
            # Add new records
            for name, record in attendance_log.items():
                df = pd.concat([df, pd.DataFrame([{
                    "Name": name,
                    "Timestamp": record['timestamp'],
                    "Status": record['status'],
                    "Day": record['day']
                }])], ignore_index=True)
            
            # Remove duplicates
            df = df.drop_duplicates(subset=['Name', 'Timestamp'], keep='last')
            df.to_excel("attendance.xlsx", index=False)
        
        time.sleep(10)

# Start background threads
threading.Thread(target=recognize_faces, daemon=True).start()
threading.Thread(target=save_attendance_periodically, daemon=True).start()

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True, port=5050)