import os
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


# Database connection
db = mysql.connector.connect(
    host=os.getenv("MYSQLHOST", "localhost"),
    port=int(os.getenv("MYSQLPORT", 3306)),
    user=os.getenv("MYSQLUSER", "root"),
    password=os.getenv("MYSQLPASSWORD", ""),
    database=os.getenv("MYSQLDATABASE", "student_db")
)

cursor = db.cursor()


# Home
@app.route("/")
def home():
    return render_template("index.html")


# Add Student
@app.route("/add", methods=["POST"])
def add_student():

    name = request.form["name"]
    email = request.form["email"]
    department = request.form["department"]
    year = request.form["year"]

    cursor.execute(
        """
        INSERT INTO students(name, email, department, year)
        VALUES(%s, %s, %s, %s)
        """,
        (name, email, department, year)
    )

    db.commit()

    return render_template("index.html")


# View Students
@app.route("/students")
def students():

    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    return render_template(
        "students.html",
        students=data
    )


# Delete Student
@app.route("/delete/<int:id>")
def delete_student(id):

    cursor.execute(
        "DELETE FROM students WHERE id=%s",
        (id,)
    )

    db.commit()

    return students()


# Update Student
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_student(id):

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        year = request.form["year"]

        cursor.execute(
            """
            UPDATE students
            SET name=%s,
                email=%s,
                department=%s,
                year=%s
            WHERE id=%s
            """,
            (name, email, department, year, id)
        )

        db.commit()

        return students()

    cursor.execute(
        "SELECT * FROM students WHERE id=%s",
        (id,)
    )

    student = cursor.fetchone()

    return render_template(
        "update_student.html",
        student=student
    )


# Run application
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=False
    )