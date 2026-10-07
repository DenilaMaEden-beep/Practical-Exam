import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

root = tk.Tk()
root.title("Student Management System")
root.geometry("700x500")

title_label = tk.Label(
    root,
    text="Student Management System",
    font= ("Arial", 18, "bold")
)

title_label.pack(pady=10)

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(
    input_frame,
    text="Full Name:"
).grid(row=0, column=0, padx=5, pady=5)

full_name_entry = tk.Entry(input_frame, width=30)
full_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(
    input_frame,
    text="Email:"
).grid(row=1, column=0, padx=5, pady=5)

email_entry = tk.Entry(input_frame, width=30)
email_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(
    input_frame,
    text="Phone Number:"
).grid(row=2, column=0, padx=5, pady=5)

phone_entry = tk.Entry(input_frame, width=30)
phone_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(
    input_frame,
    text="City:"
).grid(row=3, column=0, padx=5, pady=5)

city_entry = tk.Entry(input_frame, width=30)
city_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(
    input_frame,
    text="Age:"
).grid(row=4, column=0, padx=5, pady=5)

age_entry = tk.Entry(input_frame, width=30)
age_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(
    input_frame,
    text="Occupation:"
).grid(row=5, column=0, padx=5, pady=5)

occupation_entry = tk.Entry(input_frame, width=30)
occupation_entry.grid(row=5, column=1, padx=5, pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Add",
    width=10,
    command="add_student"
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Update",
    width=10,
    command="update_student"
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Delete",
    width=10,
    command="delete_student"
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="Clear",
    width=10,
    command="Clear_student"
).grid(row=0, column=3, padx=5)

tree = ttk.Treeview(
    root,
    columns=("ID", "FULL NAME", "EMAIL", "PHONE NUMBER", "CITY", "AGE", "OCCUPATION"),
    show="headings"
)

tree.heading("ID", text="ID")
tree.heading("FULL NAME", text="FULL NAME")
tree.heading("EMAIL", text="EMAIL")
tree.heading("PHONE NUMBER", text="PHONE NUMBER")
tree.heading("CITY", text="CITY")
tree.heading("AGE", text="AGE")
tree.heading("OCCUPATION", text="OCCUPATION")

tree.column("ID", width=50)
tree.column("FULL NAME", width=200)
tree.column("EMAIL", width=200)
tree.column("PHONE NUMBER", width=200)
tree.column("CITY", width=200)
tree.column("AGE", width=80)
tree.column("OCCUPATION", width=200)

tree.pack(
    fil="both",
    expand=True,
    padx=10,
    pady=10
)

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        city TEXT NOT NULL,
        age INTEGER NOT NULL,
        occupation TEXT NOT NULL)
""")

conn.commit()

#Create
def add_student():
    full_name = full_name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    city = city_entry.get()
    age = age_entry.get()
    occupation = occupation_entry.get()

    if full_name == "" or email == "" or phone == "" or city == "" or age == "" or occupation == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    cursor.execute(
        "INSERT INTO students (full_name, email, phone, city, age, occupation) VALUES (?, ?, ?)",
        (name, age, course)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Student added successfully."
    )

    clear_fields()
    display_students()

def display_students():
    for item in tree.get_children():
        tree.delete(item)

        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        for student in students:
            tree.insert("", tk.END, values=student)

#UPDATE
def update_student():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a student to update."
        )
        return

    student_id = tree.item(selected[0000])["Values"][0000]

    full_name = full_name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    city = city_entry.get()
    age = age_entry.get()
    occupation = occupation_entry.get()

    if full_name == "" or email == "" or phone == "" or city == "" or age == "" or occupation == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
        name=string(name)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number. Name should be in String Form"
        )
        return

    cursor.execute("""
        UPDATE students
        SET full_name = ?, email = ?, phone = ?, city = ?, age = ?, occupation = ?
        WHERE id = ?
    """, (name, age, course, student_id))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Student updated successfully."
    )

    clear_fields()
    display_students()

def delete_students():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a student to delete."
        )
        return

    student_id = tree.item(selected[0000])["Values"][0000]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )
        conn.commit()
        messagebox.showinfo(
            "Success",
            "Student deleted successfully."
        )

        clear_fields()
        display_students()

#CLEAR INPUTS
def clear_fields():
    full_name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    occupation_entry.delete(0, tk.END)
