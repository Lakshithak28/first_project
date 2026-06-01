import customtkinter as ctk
from tkinter import ttk, messagebox
import database

selected_id = None

# ---------------- FUNCTIONS ---------------- #

def clear_fields():
    name_var.set("")
    age_var.set("")
    course_var.set("")

def load_students():
    for row in tree.get_children():
        tree.delete(row)

    for student in database.get_students():
        tree.insert("", "end", values=student)

def add_student():
    if not name_var.get() or not age_var.get() or not course_var.get():
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    database.add_student(
        name_var.get(),
        age_var.get(),
        course_var.get()
    )

    load_students()
    clear_fields()

def select_student(event):
    global selected_id

    selected = tree.focus()

    if selected:
        values = tree.item(selected, "values")

        selected_id = values[0]

        name_var.set(values[1])
        age_var.set(values[2])
        course_var.set(values[3])

def update_student():
    global selected_id

    if selected_id is None:
        messagebox.showwarning("Warning", "Select a student")
        return

    database.update_student(
        selected_id,
        name_var.get(),
        age_var.get(),
        course_var.get()
    )

    load_students()
    clear_fields()

def delete_student():
    global selected_id

    if selected_id is None:
        messagebox.showwarning("Warning", "Select a student")
        return

    database.delete_student(selected_id)

    load_students()
    clear_fields()

def search_student():
    keyword = name_var.get()

    for row in tree.get_children():
        tree.delete(row)

    for student in database.search_student(keyword):
        tree.insert("", "end", values=student)

# ---------------- APP ---------------- #

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Student Management System")
root.geometry("1000x650")

title = ctk.CTkLabel(
    root,
    text="Student Management System",
    font=("Arial", 28, "bold")
)
title.pack(pady=20)

# Form Frame
form_frame = ctk.CTkFrame(root)
form_frame.pack(fill="x", padx=20, pady=10)

name_var = ctk.StringVar()
age_var = ctk.StringVar()
course_var = ctk.StringVar()

ctk.CTkLabel(form_frame, text="Name").grid(row=0, column=0, padx=10, pady=10)
ctk.CTkEntry(form_frame, textvariable=name_var, width=200).grid(row=0, column=1)

ctk.CTkLabel(form_frame, text="Age").grid(row=0, column=2, padx=10)
ctk.CTkEntry(form_frame, textvariable=age_var, width=100).grid(row=0, column=3)

ctk.CTkLabel(form_frame, text="Course").grid(row=0, column=4, padx=10)
ctk.CTkEntry(form_frame, textvariable=course_var, width=200).grid(row=0, column=5)

# Buttons
button_frame = ctk.CTkFrame(root)
button_frame.pack(fill="x", padx=20, pady=10)

ctk.CTkButton(
    button_frame,
    text="Add Student",
    command=add_student
).pack(side="left", padx=10, pady=10)

ctk.CTkButton(
    button_frame,
    text="Update Student",
    command=update_student
).pack(side="left", padx=10)

ctk.CTkButton(
    button_frame,
    text="Delete Student",
    command=delete_student
).pack(side="left", padx=10)

ctk.CTkButton(
    button_frame,
    text="Search",
    command=search_student
).pack(side="left", padx=10)

ctk.CTkButton(
    button_frame,
    text="Show All",
    command=load_students
).pack(side="left", padx=10)

# Table
table_frame = ctk.CTkFrame(root)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

columns = ("ID", "Name", "Age", "Course")

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for col in columns:
    tree.heading(col, text=col)

tree.column("ID", width=80)
tree.column("Name", width=250)
tree.column("Age", width=100)
tree.column("Course", width=250)

tree.pack(fill="both", expand=True)

tree.bind("<<TreeviewSelect>>", select_student)

load_students()

root.mainloop()