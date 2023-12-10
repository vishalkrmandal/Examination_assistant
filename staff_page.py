import tkinter as tk
from tkinter import messagebox, filedialog
import mysql.connector
from fpdf import FPDF


class EmployeeManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Employee Management System")
        self.geometry("1080x720")

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishal@123",
            database="ex"
        )
        self.cursor = self.db.cursor()

        self.create_tables()

        self.create_button("Create Employee Profile", self.create_employee_profile)
        self.create_button("View Employee Profile", self.view_employee_profile)
        self.create_button("Generate Student Result", self.generate_student_result)
        self.create_button("Exit", self.exit_program)

    def create_tables(self):
        employees_query = """
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INT PRIMARY KEY,
            name VARCHAR(255),
            designation VARCHAR(255),
            department VARCHAR(255),
            batch VARCHAR(255)
        )
        """
        self.cursor.execute(employees_query)
        self.db.commit()

        marks_query = """
        CREATE TABLE IF NOT EXISTS marks (
            student_id INT PRIMARY KEY NOT NULL,
            student_name CHAR(50) NOT NULL,
            subject VARCHAR(255),
            marks FLOAT
        )
        """
        self.cursor.execute(marks_query)
        self.db.commit()

    def create_employee_profile(self):
        profile_window = tk.Toplevel(self)
        profile_window.title("Create Employee Profile")
        profile_window.geometry("500x300")

        employee_id_label = tk.Label(profile_window, text="Employee ID:")
        employee_id_label.pack()
        employee_id_entry = tk.Entry(profile_window)
        employee_id_entry.pack()

        name_label = tk.Label(profile_window, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(profile_window)
        name_entry.pack()

        designation_label = tk.Label(profile_window, text="Designation:")
        designation_label.pack()
        designation_entry = tk.Entry(profile_window)
        designation_entry.pack()

        department_label = tk.Label(profile_window, text="Department:")
        department_label.pack()
        department_entry = tk.Entry(profile_window)
        department_entry.pack()

        batch_label = tk.Label(profile_window, text="Batch:")
        batch_label.pack()
        batch_entry = tk.Entry(profile_window)
        batch_entry.pack()

        save_button = tk.Button(profile_window, text="Save", command=lambda: self.save_employee_profile(
            employee_id_entry.get(),
            name_entry.get(),
            designation_entry.get(),
            department_entry.get(),
            batch_entry.get(),
            profile_window
        ))
        save_button.pack()

    def save_employee_profile(self, employee_id, name, designation, department, batch, window):
        query = "INSERT INTO employees (employee_id, name, designation, department, batch) VALUES (%s, %s, %s, %s, %s)"
        values = (employee_id, name, designation, department, batch)
        self.cursor.execute(query, values)
        self.db.commit()
        messagebox.showinfo("Create Employee Profile", "Employee profile created successfully!")
        window.destroy()

    def view_employee_profile(self):
        profile_window = tk.Toplevel(self)
        profile_window.title("View Employee Profile")
        profile_window.geometry("300x200")

        employee_id_label = tk.Label(profile_window, text="Employee ID:")
        employee_id_label.pack()
        employee_id_entry = tk.Entry(profile_window)
        employee_id_entry.pack()

        view_button = tk.Button(profile_window, text="View", command=lambda: self.fetch_employee_profile(
            employee_id_entry.get(),
            profile_window
        ))
        view_button.pack()

    def fetch_employee_profile(self, employee_id, window):
        query = "SELECT * FROM employees WHERE employee_id = %s"
        values = (employee_id,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()

        if result:
            messagebox.showinfo("View Employee Profile",
                                f"Employee ID: {result[0]}\n"
                                f"Name: {result[1]}\n"
                                f"Designation: {result[2]}\n"
                                f"Department: {result[3]}\n"
                                f"Batch: {result[4]}")
        else:
            messagebox.showinfo("View Employee Profile", "No employee profile found for the given ID.")
        window.destroy()

    def generate_student_result(self):
        result_window = tk.Toplevel(self)
        result_window.title("Generate Student Result")
        result_window.geometry("300x200")

        student_id_label = tk.Label(result_window, text="Student ID:")
        student_id_label.pack()
        student_id_entry = tk.Entry(result_window)
        student_id_entry.pack()

        generate_button = tk.Button(result_window, text="Generate", command=lambda: self.fetch_student_result(
            student_id_entry.get(),
            result_window
        ))
        generate_button.pack()

    def fetch_student_result(self, student_id, window):
        query = "SELECT student_name, subject, marks FROM marks WHERE student_id = %s"
        values = (student_id,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()

        if result:
            total_marks = 0
            result_text = "Student Result:\n"
            student_name = ""  # Initialize student_name variable

            for i, row in enumerate(result):
                if i == 0:
                    student_name = row[0]  # Assign student_name only for the first row
                subject = row[1]
                marks = row[2]
                total_marks += marks
                result_text += f"\nSubject: {subject}\nMarks: {marks}"

            result_text = f"Name: {student_name}\n" + result_text  # Prepend student_name to result_text

            percentage = (total_marks / (len(result) * 100)) * 100
            result_text += f"\nTotal Marks: {total_marks}\nPercentage: {percentage:.2f}%"

            # Show result in messagebox
            messagebox.showinfo("Generate Student Result", result_text)

            # Ask for PDF download
            download_pdf = messagebox.askyesno("Download PDF", "Do you want to download the result as a PDF?")
            if download_pdf:
                self.generate_pdf_result(student_id, result)

        else:
            messagebox.showinfo("Generate Student Result", "No marks found for the student.")
        window.destroy()

    def generate_pdf_result(self, student_id, result):
        pdf = FPDF()

        # Set up PDF
        pdf.set_font("Arial", "B", 16)
        pdf.add_page()

        # Add result information
        pdf.cell(0, 10, "Student Result", ln=True, align="C")
        pdf.cell(0, 10, f"Student ID: {student_id}", ln=True, align="L")
        pdf.cell(0, 10, "", ln=True)

        student_name = ""  # Initialize student_name variable

        for i, row in enumerate(result):
            if i == 0:
                student_name = row[0]  # Assign student_name only for the first row
            subject = row[1]
            marks = row[2]
            pdf.cell(0, 10, f"Subject: {subject}", ln=True, align="L")
            pdf.cell(0, 10, f"Marks: {marks}", ln=True, align="L")
            pdf.cell(0, 10, "", ln=True)

        total_marks = sum([row[2] for row in result])
        percentage = (total_marks / (len(result) * 100)) * 100
        pdf.cell(0, 10, f"Name: {student_name}", ln=True, align="L")  # Print student_name
        pdf.cell(0, 10, f"Total Marks: {total_marks}", ln=True, align="L")
        pdf.cell(0, 10, f"Percentage: {percentage:.2f}%", ln=True, align="L")

        # Save PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            pdf.output(file_path)
            messagebox.showinfo("Save PDF", "PDF saved successfully!")


    def exit_program(self):
        self.cursor.close()
        self.db.close()
        self.destroy()

    def create_button(self, text, command):
        button = tk.Button(self, text=text, command=command)
        button.pack(pady=10)

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = EmployeeManagementSystem()
    app.run()
