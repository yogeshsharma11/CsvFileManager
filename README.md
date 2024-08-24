Project Name
CSV File Manager

Project Description
This project is a Django-based web application that allows users to log in or sign up, upload CSV files, and manage the data within these files. Users can view, edit, and update data directly through the web interface. The application also supports exporting the updated data back to a CSV file. Pagination is implemented to manage multiple file uploads, and the interface is designed to be user-friendly and visually appealing.

Features
User Authentication: Login and signup functionality using Django's built-in authentication system.
CSV File Upload: Users can upload CSV files, which are stored in the database.
Data Display: Uploaded data is displayed in a table format, with options to edit existing rows or add new rows.
Data Editing: Users can update or insert new data rows without deleting existing data.
Pagination: If more than 10 files are uploaded by a user, pagination is provided to navigate through the files.
API Endpoints: Includes API endpoints for login, signup, and CSV upload.
Responsive UI: A well-designed, responsive user interface for an enhanced user experience.

Technologies Used
Django (Python Web Framework)
HTML/CSS (Frontend)
SQLite (Default Django database)


Installation Instructions
Clone the repository:
->bash
git clone <repository-url>

->bash
cd CvsUploader1

->bash
python3 -m venv env

->Install the required dependencies:
pip install -r requirements.txt

->Apply migrations to set up the database:
python manage.py migrate

->Run the development server:
python manage.py runserver
Usage Instructions

Access the application in your web browser:
->http://127.0.0.1:8000/
