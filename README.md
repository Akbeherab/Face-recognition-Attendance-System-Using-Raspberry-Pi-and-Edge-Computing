# Face-recognition-Attendance-System-Using-Raspberry-Pi-and-Edge-Computing

[System Demo](demo.gif)


A complete automated attendance tracking system using real-time face recognition technology, built with Python, Flask, and OpenCV. This system eliminates manual attendance processes by automatically detecting and recognizing students' faces, marking attendance with timestamps, and generating detailed reports.


## Features

### Core Functionality
- **Real-time Face Detection**: Uses OpenCV and dlib for live face detection
- **Face Recognition**: Compares detected faces with pre-registered student encodings
- **Automated Attendance Tracking**: Marks attendance automatically when recognized
- **Time-based Status Classification**: Identifies students as "On Time" or "Late" based on configurable thresholds

### User Management
- **Admin Authentication**: Secure login system for administrators
- **Student Enrollment**: Web interface for registering new students with photos
- **Student Profiles**: Stores comprehensive student information (name, ID, department, contact)

### Reporting
- **Real-time Dashboard**: Displays current attendance status
- **Excel Export**: Download attendance records in spreadsheet format
- **PDF Reports**: Generate printable attendance reports
- **Daily/Weekly Views**: Filter attendance by time periods

### System Configuration
- **Time Limit Settings**: Adjust cutoff time for "On Time" status
- **Camera Configuration**: Supports multiple camera sources
- **Data Backup**: Automatic saving of attendance records

## Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask**: Web application framework
- **OpenCV**: Computer vision processing
- **face_recognition**: Face detection and recognition library
- **Pandas**: Data manipulation and reporting


### Frontend
- **HTML5**: Page structure
- **CSS3**: Styling and animations

### Additional Tools
- **pdfkit**: PDF report generation
- **Werkzeug**: Security and authentication
- **Flask-Login**: Session management

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- wkhtmltopdf (for PDF generation)

   cd face-recognition-attendance
