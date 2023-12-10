import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
#from tkinter import Toplevel, Label, Entry, Button, messagebox


class RegistrationForm(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.iconbitmap(r'E:\WORK\PYTHON PROJECT EXORM\exorm.ico')
        self.title("Registration Form")
        self.geometry("1080x720")

        # Create registration form widgets
        self.first_name_label = tk.Label(self, text="First Name:")
        self.first_name_edit = tk.Entry(self)
        self.middle_name_label = tk.Label(self, text="Middle Name:")
        self.middle_name_edit = tk.Entry(self)
        self.last_name_label = tk.Label(self, text="Last Name:")
        self.last_name_edit = tk.Entry(self)
        self.email_label = tk.Label(self, text="Email:")
        self.email_edit = tk.Entry(self)
        self.gender_label = tk.Label(self, text="Gender:")
        self.gender_combo = ttk.Combobox(self, values=["Male", "Female", "Other"])
        self.designation_label = tk.Label(self, text="Designation:")
        self.designation_combo = ttk.Combobox(self, values=["Staff", "Faculty"])
        self.password_label = tk.Label(self, text="Password:")
        self.password_edit = tk.Entry(self, show="*")
        self.confirm_password_label = tk.Label(self, text="Confirm Password:")
        self.confirm_password_edit = tk.Entry(self, show="*")
        self.register_button = tk.Button(self, text="Register", command=self.register)

        # Configure widget sizes
        self.first_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.first_name_edit.grid(row=0, column=1, padx=10, pady=10)
        self.middle_name_label.grid(row=1, column=0, padx=10, pady=10)
        self.middle_name_edit.grid(row=1, column=1, padx=10, pady=10)
        self.last_name_label.grid(row=2, column=0, padx=10, pady=10)
        self.last_name_edit.grid(row=2, column=1, padx=10, pady=10)
        self.email_label.grid(row=3, column=0, padx=10, pady=10)
        self.email_edit.grid(row=3, column=1, padx=10, pady=10)
        self.gender_label.grid(row=4, column=0, padx=10, pady=10)
        self.gender_combo.grid(row=4, column=1, padx=10, pady=10)
        self.designation_label.grid(row=5, column=0, padx=10, pady=10)
        self.designation_combo.grid(row=5, column=1, padx=10, pady=10)
        self.password_label.grid(row=6, column=0, padx=10, pady=10)
        self.password_edit.grid(row=6, column=1, padx=10, pady=10)
        self.confirm_password_label.grid(row=7, column=0, padx=10, pady=10)
        self.confirm_password_edit.grid(row=7, column=1, padx=10, pady=10)
        self.register_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)


    def register(self):
        first_name = self.first_name_edit.get()
        middle_name = self.middle_name_edit.get()
        last_name = self.last_name_edit.get()
        email = self.email_edit.get()
        gender = self.gender_combo.get()
        designation = self.designation_combo.get()
        password = self.password_edit.get()
        confirm_password = self.confirm_password_edit.get()

        # Validate password match
        if password != confirm_password:
            messagebox.showwarning("Error", "Passwords do not match!")
            return

        # Connect to MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishal@123",
            database="ex",
            auth_plugin='mysql_native_password',

        )
        cursor = db.cursor()
        s="""
        CREATE TABLE IF NOT EXISTS registrations(
                first_name varchar(20),
                middle_name varchar(20),
                last_name varchar(20),
                email varchar(50) PRIMARY KEY NOT NULL,
                gender varchar(20),
                designation varchar(100),
                password varchar(50)
                )
                """
        cursor.execute(s)

    

        # Insert the registration details into the database
        query = "INSERT INTO registrations (first_name, middle_name, last_name, email, gender, designation, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (first_name, middle_name, last_name, email, gender, designation, password)

        try:
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Success", "Registration successful!")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Error occurred: {error}")

        # Close database connection
        db.close()


if __name__ == "__main__":
    registration_form = RegistrationForm()
    registration_form.mainloop()
