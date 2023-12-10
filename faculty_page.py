import tkinter as tk
from tkinter import messagebox
import mysql.connector

class TeacherManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.iconbitmap(r'E:\WORK\PYTHON PROJECT EXORM\exorm.ico')
        self.title("Teacher Management System")
        self.geometry("1080x720")
        self.create_widgets()
        self.connect_database()

    def connect_database(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishal@123",
            database="ex"
        )
        self.cursor = self.db.cursor()

    
        self.teachers_query = """
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INT PRIMARY KEY,
            name VARCHAR(255),
            subject VARCHAR(255),
            school VARCHAR(255),
            batch VARCHAR(255)
        )
        """
        self.cursor.execute(self.teachers_query)
        print("Table 'teachers' created successfully!")

        self.marks_query = """
        CREATE TABLE IF NOT EXISTS marks(
            student_id VARCHAR(255),
            student_name CHAR(50) NOT NULL,
            subject VARCHAR(255),
            marks FLOAT
        )
        """
        self.cursor.execute(self.marks_query)
        print("Table 'marks' created successfully!")


    def create_widgets(self):
        self.label = tk.Label(self, text="------ Teacher Management System ------")
        self.label.pack()

        self.button1 = tk.Button(self, text="1. Create Teacher Profile", command=self.create_profile_window)
        self.button1.pack()

        self.button2 = tk.Button(self, text="2. View Teacher Profile", command=self.view_profile_window)
        self.button2.pack()

        self.button3 = tk.Button(self, text="3. Upload Marks", command=self.upload_marks_window)
        self.button3.pack()

        self.button4 = tk.Button(self, text="4. View Marks", command=self.view_marks_window)
        self.button4.pack()

        self.button0 = tk.Button(self, text="0. Exit", command=self.quit)
        self.button0.pack()

    def create_profile_window(self):
        self.profile_window = tk.Toplevel(self)
        self.profile_window.title("Create Teacher Profile")
        self.profile_window.geometry("400x300")

        self.teacher_id_label = tk.Label(self.profile_window, text="Teacher ID:")
        self.teacher_id_label.pack()
        self.teacher_id_entry = tk.Entry(self.profile_window)
        self.teacher_id_entry.pack()

        self.name_label = tk.Label(self.profile_window, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.profile_window)
        self.name_entry.pack()

        self.subject_label = tk.Label(self.profile_window, text="Subject:")
        self.subject_label.pack()
        self.subject_entry = tk.Entry(self.profile_window)
        self.subject_entry.pack()

        self.school_label = tk.Label(self.profile_window, text="School:")
        self.school_label.pack()
        self.school_entry = tk.Entry(self.profile_window)
        self.school_entry.pack()

        self.batch_label = tk.Label(self.profile_window, text="Batch:")
        self.batch_label.pack()
        self.batch_entry = tk.Entry(self.profile_window)
        self.batch_entry.pack()

        self.create_profile_button = tk.Button(self.profile_window, text="Create Profile", command=self.create_profile)
        self.create_profile_button.pack()

    def create_profile(self):
        teacher_id = self.teacher_id_entry.get()
        name = self.name_entry.get()
        subject = self.subject_entry.get()
        school = self.school_entry.get()
        batch = self.batch_entry.get()

        query = "INSERT INTO teachers (teacher_id, name, subject, school, batch) VALUES (%s, %s, %s, %s, %s)"
        values = (teacher_id, name, subject, school, batch)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Create Teacher Profile", "Teacher profile created successfully!")
        except mysql.connector.Error as error:
            messagebox.showerror("Create Teacher Profile", f"Error occurred: {error}")

    def upload_marks_window(self):
        self.upload_marks_window = tk.Toplevel(self)
        self.upload_marks_window.title("Upload Marks")
        self.upload_marks_window.geometry("400x300")

        self.student_id_label = tk.Label(self.upload_marks_window, text="Student ID:")
        self.student_id_label.pack()
        self.student_id_entry = tk.Entry(self.upload_marks_window)
        self.student_id_entry.pack()

        self.student_name_label = tk.Label(self.upload_marks_window, text="Student Name:")
        self.student_name_label.pack()
        self.student_name_entry = tk.Entry(self.upload_marks_window)
        self.student_name_entry.pack()

        self.subject_label = tk.Label(self.upload_marks_window, text="Subject:")
        self.subject_label.pack()
        self.subject_entry = tk.Entry(self.upload_marks_window)
        self.subject_entry.pack()

        self.marks_label = tk.Label(self.upload_marks_window, text="Marks:")
        self.marks_label.pack()
        self.marks_entry = tk.Entry(self.upload_marks_window)
        self.marks_entry.pack()

        self.upload_marks_button = tk.Button(self.upload_marks_window, text="Upload Marks", command=self.upload_marks)
        self.upload_marks_button.pack()

    def upload_marks(self):
        student_id = self.student_id_entry.get()
        student_name = self.student_name_entry.get()
        subject = self.subject_entry.get()
        marks = self.marks_entry.get()

        query = "INSERT INTO marks (student_id, student_name, subject, marks) VALUES (%s, %s, %s, %s)"
        values = (student_id, student_name, subject, marks)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Upload Marks", "Marks uploaded successfully!")
        except mysql.connector.Error as error:
            messagebox.showerror("Upload Marks", f"Error occurred: {error}")

    def view_profile_window(self):
        self.view_profile_window = tk.Toplevel(self)
        self.view_profile_window.title("View Teacher Profile")
        self.view_profile_window.geometry("400x200")

        self.teacher_id_label = tk.Label(self.view_profile_window, text="Teacher ID:")
        self.teacher_id_label.pack()
        self.teacher_id_entry = tk.Entry(self.view_profile_window)
        self.teacher_id_entry.pack()

        self.view_profile_button = tk.Button(self.view_profile_window, text="View Profile", command=self.view_profile)
        self.view_profile_button.pack()

    def view_profile(self):
        teacher_id = self.teacher_id_entry.get()
        query = "SELECT * FROM teachers WHERE teacher_id = %s"
        values = (teacher_id,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()

        if result:
            messagebox.showinfo(
                "View Teacher Profile",
                f"Teacher Profile:\n\nTeacher ID: {result[0]}\nName: {result[1]}\nSubject: {result[2]}\nSchool: {result[3]}\nBatch: {result[4]}"
            )
        else:
            messagebox.showinfo("View Teacher Profile", "No teacher profile found for the given ID.")

    def view_marks_window(self):
        self.view_marks_window = tk.Toplevel(self)
        self.view_marks_window.title("View Marks")
        self.view_marks_window.geometry("400x200")

        self.student_id_label = tk.Label(self.view_marks_window, text="Student ID:")
        self.student_id_label.pack()
        self.student_id_entry = tk.Entry(self.view_marks_window)
        self.student_id_entry.pack()

        self.view_marks_button = tk.Button(self.view_marks_window, text="View Marks", command=self.view_marks)
        self.view_marks_button.pack()

    def view_marks(self):
        student_id = self.student_id_entry.get()
        query = "SELECT student_name, subject, marks FROM marks WHERE student_id = %s"
        values = (student_id,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        if len(result) > 0:
            marks_info = ""
            for row in result:
                marks_info += f"Name: {row[0]}\nSubject: {row[1]}\nMarks: {row[2]}\n\n"
            messagebox.showinfo("View Marks", marks_info)
        else:
            messagebox.showinfo("View Marks", "No marks found for the student.")

    def quit(self):
        self.cursor.close()
        self.db.close()
        self.destroy()

if __name__ == "__main__":
    app = TeacherManagementSystem()
    app.mainloop()
