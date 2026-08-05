from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nandu@123",
    database="student_db"
)

cursor = db.cursor()


@app.route("/")
def home():
    return render_template("index.html")


# Add Student
@app.route("/add", methods=["POST"])
def add_student():

    name = request.form["name"]
    parent_name = request.form["parent_name"]
    mobile = request.form["mobile"]
    email = request.form["email"]
    department = request.form["department"]
    year = request.form["year"]
    attendance = request.form["attendance"]

    cursor.execute(
        """
        INSERT INTO students
        (name,parent_name,mobile,email,department,year,attendance)
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        """,
        (name, parent_name, mobile, email, department, year, attendance)
    )

    db.commit()

    return render_template("index.html")


# View Students
@app.route("/students")
def students():

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    return render_template("students.html", students=data)


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
        parent_name = request.form["parent_name"]
        mobile = request.form["mobile"]
        email = request.form["email"]
        department = request.form["department"]
        year = request.form["year"]
        attendance = request.form["attendance"]

        cursor.execute("""
            UPDATE students
            SET
                name=%s,
                parent_name=%s,
                mobile=%s,
                email=%s,
                department=%s,
                year=%s,
                attendance=%s
            WHERE id=%s
        """,
        (name, parent_name, mobile, email, department, year, attendance, id))

        db.commit()

        return students()

    cursor.execute(
        "SELECT * FROM students WHERE id=%s",
        (id,)
    )

    student = cursor.fetchone()

    return render_template("update_student.html", student=student)


if __name__ == "__main__":
    app.run(debug=True)