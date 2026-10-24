# Student Management System

A beginner-friendly web application built with Python, Flask, and MySQL to manage student records.

## Features

- Add new students
- View all student records
- Edit existing student information
- Delete student records
- Validate required fields
- Prevent duplicate student IDs
- Display success and error messages
- Store data in a MySQL database

## Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS
- **Database:** MySQL
- **Database Connector:** MySQL Connector/Python
- **Configuration:** python-dotenv

## Project Structure

```text
student-management-system/
├── app.py
├── database.sql
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   ├── add_student.html
│   ├── students.html
│   └── edit_student.html
└── static/
    └── style.css
```

## Requirements

- Python 3
- MySQL Server
- A web browser

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd student-management-system
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository URL.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows Command Prompt:

```cmd
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the database

Open MySQL Workbench and execute the SQL statements in `database.sql`.

### 5. Configure environment variables

Create a `.env` file in the project root by copying `.env.example`.

Add your own MySQL credentials and a long, random secret key. Never commit your `.env` file.

### 6. Run the application

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Learning Objectives

This project demonstrates the fundamentals of full-stack web development, including:

- Connecting a Flask backend to a MySQL database
- Handling HTML form submissions
- Implementing CRUD operations
- Executing SQL queries from Python
- Managing configuration through environment variables
- Organizing templates and static files

## Future Improvements

- Search and filter student records
- Pagination
- User authentication
- Improved form validation
- Deployment to a hosting platform

## Author

CSE Student | Aspiring Full-Stack Software Developer