import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age TEXT,
    course TEXT
)
""")

conn.commit()

def add_student(name, age, course):
    cursor.execute(
        "INSERT INTO students(name, age, course) VALUES (?, ?, ?)",
        (name, age, course)
    )
    conn.commit()

def get_students():
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()

def delete_student(student_id):
    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (student_id,)
    )
    conn.commit()

def search_student(keyword):
    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        ('%' + keyword + '%',)
    )
    return cursor.fetchall()

def update_student(student_id, name, age, course):
    cursor.execute("""
    UPDATE students
    SET name=?, age=?, course=?
    WHERE id=?
    """, (name, age, course, student_id))
    conn.commit()
    