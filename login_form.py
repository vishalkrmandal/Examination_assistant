import mysql.connector
from tkinter import Tk, Label, Entry, Button, messagebox
from registration_form import RegistrationForm
from faculty_page import TeacherManagementSystem
from staff_page import EmployeeManagementSystem


class LoginForm(Tk):
    def __init__(self):
        super().__init__()
        #self.iconbitmap(r'E:\WORK\PYTHON PROJECT EXORM\exorm.ico')
        self.title("Login Form")
        self.geometry("1080x720")

        # Create login form widgets
        self.email_label = Label(self, text="Email:")
        self.email_entry = Entry(self)
        self.password_label = Label(self, text="Password:")
        self.password_entry = Entry(self, show="*")
        self.login_button = Button(self, text="Login", command=self.login)
        self.forget_password_button = Button(self,text="Forgot Password", command=self.forget_password)
        self.register_button = Button(self, text="Registration", command=self.open_registration)

        # Configure widget sizes
        self.email_label.configure(font=("Helvetica", 12))
        self.email_entry.configure(font=("Helvetica", 12), width=30)
        self.password_label.configure(font=("Helvetica", 12))
        self.password_entry.configure(font=("Helvetica", 12), width=30)
        self.login_button.configure(font=("Helvetica", 12), width=20)
        self.forget_password_button.configure(font=("Helvetica", 12), width=20)
        self.register_button.configure(font=("Helvetica", 12), width=20)

        # Pack widgets
        self.email_label.pack()
        self.email_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.login_button.pack()
        self.forget_password_button.pack()
        self.register_button.pack()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

         # Connect to MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishal@123",
            database="ex"
        )
        cursor = db.cursor()

        # Check if the user exists and retrieve the designation
        query = "SELECT designation FROM registrations WHERE email = %s AND password = %s"
        values = (email, password)

        cursor.execute(query, values)
        result = cursor.fetchone()

        if result is None:
            messagebox.showwarning("Login Error", "Invalid email or password!")
        else:
            designation = result[0]
            if designation == "Staff":
                messagebox.showinfo("Login Successful", "Logged in as Staff.")
                staff_page = EmployeeManagementSystem()
                self.withdraw()  # Hide the login form
                staff_page.wait_window()  # Wait for the staff page to be closed
                self.deiconify()  # Show the login form again

            elif designation == "Faculty":
                messagebox.showinfo("Login Successful", "Logged in as Faculty.")
                faculty_page = TeacherManagementSystem()
                self.withdraw()  # Hide the login form
                faculty_page.wait_window()  # Wait for the faculty page to be closed
                self.deiconify()  # Show the login form again


        # Close database connection
        db.close()

    def forget_password(self):
        messagebox.showinfo("Forgot Password", "Please contact the administrator to reset your password.")

    def open_registration(self):
        registration_form = RegistrationForm()
        self.withdraw()  # Hide the login form
        registration_form.wait_window()  # Wait for the registration form to be closed
        self.deiconify()  # Show the login form again


if __name__ == "__main__":
    app = LoginForm()
    app.mainloop()
