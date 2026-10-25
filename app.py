import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import IntegrityError

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "student_management"),
    "ssl_ca": os.getenv("DB_SSL_CA") or None
}


# Connect to MySQL
def get_connection():
    return mysql.connector.connect(**db_config)


# Home page: Add a student
@app.route("/")
def home():
    return render_template("add_student.html")


# View all students
@app.route("/students")
def students():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM students ORDER BY student_id"
        )
        student_records = cursor.fetchall()

        return render_template(
            "students.html",
            students=student_records
        )

    except mysql.connector.Error:
        flash("Could not load student records.", "error")
        return redirect(url_for("home"))

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# Add a new student
@app.route("/add", methods=["POST"])
def add_student():
    student_id = request.form.get("student_id", "").strip()
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    department = request.form.get("department", "").strip()

    # Validate required fields
    if not all([student_id, full_name, email, department]):
        flash("Please fill in all fields.", "error")
        return redirect(url_for("home"))

    # Validate department
    if department not in ["CSE", "EEE", "BBA"]:
        flash("Please select a valid department.", "error")
        return redirect(url_for("home"))

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO students
            (student_id, full_name, email, department)
            VALUES (%s, %s, %s, %s)
        """

        values = (student_id, full_name, email, department)

        cursor.execute(query, values)
        connection.commit()

        flash("Student added successfully!", "success")

        # After saving, go directly to the students table
        return redirect(url_for("students"))

    except IntegrityError:
        flash(
            "This Student ID already exists. Please use a unique ID.",
            "error"
        )
        return redirect(url_for("home"))

    except mysql.connector.Error:
        flash(
            "Could not save the student. Please check the database connection.",
            "error"
        )
        return redirect(url_for("home"))

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# Edit an existing student
@app.route("/edit/<student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        if request.method == "POST":
            full_name = request.form.get("full_name", "").strip()
            email = request.form.get("email", "").strip()
            department = request.form.get("department", "").strip()

            if not all([full_name, email, department]):
                flash("Please fill in all fields.", "error")
                return redirect(
                    url_for("edit_student", student_id=student_id)
                )

            if department not in ["CSE", "EEE", "BBA"]:
                flash("Please select a valid department.", "error")
                return redirect(
                    url_for("edit_student", student_id=student_id)
                )

            cursor.execute(
                """
                UPDATE students
                SET full_name = %s,
                    email = %s,
                    department = %s
                WHERE student_id = %s
                """,
                (full_name, email, department, student_id)
            )

            connection.commit()

            if cursor.rowcount == 0:
                cursor.execute(
                    "SELECT student_id FROM students WHERE student_id = %s",
                    (student_id,)
                )

                if not cursor.fetchone():
                    flash("Student not found.", "error")
                    return redirect(url_for("students"))

            flash("Student updated successfully!", "success")
            return redirect(url_for("students"))

        # GET request: load existing student information
        cursor.execute(
            "SELECT * FROM students WHERE student_id = %s",
            (student_id,)
        )
        student = cursor.fetchone()

        if not student:
            flash("Student not found.", "error")
            return redirect(url_for("students"))

        return render_template(
            "edit_student.html",
            student=student
        )

    except mysql.connector.Error:
        flash("A database error occurred while editing the student.", "error")
        return redirect(url_for("students"))

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# Delete a student
@app.route("/delete/<student_id>", methods=["POST"])
def delete_student(student_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM students WHERE student_id = %s",
            (student_id,)
        )

        connection.commit()

        if cursor.rowcount > 0:
            flash("Student deleted successfully.", "success")
        else:
            flash("Student not found.", "error")

    except mysql.connector.Error:
        flash("Could not delete the student.", "error")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

    return redirect(url_for("students"))


# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)
