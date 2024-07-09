import random
import sqlite3
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
from twilio.rest import Client

# Connect to the database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create the admin table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS admin (
    user_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    secret_key TEXT NOT NULL,
    encrypted_password TEXT NOT NULL,
    date_of_joining DATE NOT NULL,
    mobile_number TEXT
)''')

# Create the patient table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS patient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_id TEXT NOT NULL,
    secret_key TEXT NOT NULL,
    encrypted_password TEXT NOT NULL,
    mobile_number TEXT
)''')

conn.commit()

class Share:
    def __init__(self):
        self.user_type = None
        # Twilio client initialization
        self.account_sid = 'account sid'
        self.auth_token = 'auth token'
        self.twilio_client = Client(self.account_sid, self.auth_token)
        self.twilio_number = 'twilio number'

    def main_menu(self):
        while True:
            print("\nMain Menu")
            print("1. Admin \n2. Patient \n3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.admin_menu()
            elif choice == '2':
                self.patient_menu()
            elif choice == '3':
                print("Exiting the application...")
                break
            else:
                print("Invalid choice. Please try again.")

    def admin_menu(self):
        while True:
            print("\nAdmin Menu")
            print("1. Admin Login \n2. Admin Signup \n3. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.login_admin()
            elif choice == '2':
                self.signup_admin()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    def patient_menu(self):
        while True:
            print("\nPatient Menu")
            print("1. Patient Login \n2. Patient Signup \n3. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.login_patient()
            elif choice == '2':
                self.signup_patient()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    def login_admin(self):
        user_id = input("Enter your Admin user ID: ")
        pass_user = input("Enter your password: ")

        c.execute("SELECT * FROM admin WHERE user_id = ?", (user_id,))
        admin = c.fetchone()

        if admin:
            _, name, secret_key, encrypted_password, _, mobile_number = admin
            decrypted_password = self.decrypt_password(encrypted_password, secret_key)
            if decrypted_password == pass_user:
                print(f"Welcome, {name}! Admin login successful")
                self.send_sms(mobile_number, f"Hello {name} {user_id}  Thanks for logging in ")
                self.admin_operations()
            else:
                print("Incorrect Password")
        else:
            print("Admin user not found")

    def admin_operations(self):
        while True:
            print("\nAdmin Operations")
            print("1. View Patients \n2. View Patient Details \n3. Back to Admin Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.view_patients()
            elif choice == '2':
                self.view_patient_details()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    def signup_admin(self):
        name = input("Enter your name: ")
        password = input("Enter your password: ")
        mobile_number = input("Enter your mobile number: ")
        date_of_join = input("Enter date of joining (YYYY-MM-DD): ")

        encrypted_password, secret_key = self.encrypt_password(password)
        user_id = self.generate_user_id()

        c.execute('''INSERT INTO admin(user_id, name, secret_key, encrypted_password, date_of_joining, mobile_number)
                     VALUES (?, ?, ?, ?, ?, ?)''', (user_id, name, secret_key, encrypted_password, date_of_join, mobile_number))
        conn.commit()
        print(f"Admin signed up successfully with USER ID: {user_id}")
        self.send_sms(mobile_number, f"Hello {name} Welcome to our app . Your USER ID: {user_id}")


    def login_patient(self):
        user_id = input("Enter your Patient user ID: ")
        pass_user = input("Enter your password: ")

        c.execute("SELECT * FROM patient WHERE user_id = ?", (user_id,))
        patient = c.fetchone()

        if patient:
            _, name, _, secret_key, encrypted_password, mobile_number = patient
            decrypted_password = self.decrypt_password(encrypted_password, secret_key)
            if decrypted_password == pass_user:
                print(f"Welcome, {name}! Patient login successful")
                self.send_sms(mobile_number, f"Hello {name}  {user_id} Thanks for logging in ")
                self.patient_operations(user_id)
            else:
                print("Incorrect Password")
        else:
            print("Patient user not found")

    def patient_operations(self, user_id):
        while True:
            print("\nPatient Operations")
            print("1. Add Appointment \n2. View Appointment \n3. Back to Patient Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_appointment(user_id)
            elif choice == '2':
                self.view_appointments(user_id)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")
                
    def signup_patient(self):
            name = input("Enter your name: ")
            password = input("Enter your password: ")
            mobile_number = input("Enter your mobile number: ")

            # Generate a unique user_id for the patient
            user_id = self.generate_user_id()

            # Encrypt the password and generate a secret key
            encrypted_password, secret_key = self.encrypt_password(password)

            # Insert the patient record into the database
            c.execute('''INSERT INTO patient(name, user_id, secret_key, encrypted_password, mobile_number)
                         VALUES (?, ?, ?, ?, ?)''', (name, user_id, secret_key, encrypted_password, mobile_number))
            conn.commit()

            # Create a table to store appointments for this patient
            # Prepend 'user_' to ensure the table name starts with a letter
            table_name = f'user_{user_id}'
            c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                details TEXT NOT NULL
            )''')
            conn.commit()

            print(f"Patient signed up successfully with USER ID: {user_id}")
            self.send_sms(mobile_number, f"Hello {name} Welcome to our app . Your USER ID: {user_id}")


    def add_appointment(self, user_id):
        # Fetch the mobile number for the given user ID
        c.execute("SELECT mobile_number FROM patient WHERE user_id = ?", (user_id,))
        result = c.fetchone()
        if result:
            mobile_number = result[0]

            appointment_date = input("Enter appointment date (YYYY-MM-DD): ")
            appointment_details = input("Enter appointment details: ")

            # Send SMS notification
            self.send_sms(mobile_number, f"Hello {user_id}, your appointment is scheduled on {appointment_date} with details: {appointment_details}")

            # Ensure table exists for the patient's appointments
            # Prepend 'user_' to ensure the table name starts with a letter
            table_name = f'user_{user_id}'
            c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date TEXT NOT NULL,
                            details TEXT NOT NULL
                        )''')

            c.execute(f'''INSERT INTO {table_name} (date, details) 
                          VALUES (?, ?)''', (appointment_date, appointment_details))
            conn.commit()
            print("Appointment added successfully.")
        else:
            print(f"No patient found with user ID {user_id}")



    def view_appointments(self, user_id):
        # Prepend 'user_' to ensure the table name starts with a letter
        table_name = f'user_{user_id}'

        c.execute(f'''SELECT date, details FROM {table_name}''')
        appointments = c.fetchall()
        if appointments:
            print(f"Appointments for User ID {user_id}:")
            for appointment in appointments:
                print(f"Date: {appointment[0]}, Details: {appointment[1]}")
        else:
            print(f"No appointments found for User ID {user_id}.")

    def view_patients(self):
        c.execute("SELECT user_id, name, mobile_number FROM patient")
        patients = c.fetchall()
        if patients:
            print("List of Patients:")
            for patient in patients:
                print(f"User ID: {patient[0]}, Name: {patient[1]}, Mobile Number: {patient[2]}")
        else:
            print("No patients found.")

    def view_patient_details(self):
        user_id = input("Enter the Patient User ID: ")
        c.execute("SELECT name, mobile_number, user_id FROM patient WHERE user_id = ?", (user_id,))
        patient = c.fetchone()
        if patient:
            print(f"Name: {patient[0]}, Mobile Number: {patient[1]}, User ID: {patient[2]}")
            self.view_appointments(user_id)
        else:
            print("Patient not found.")

    def encrypt_password(self, password):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(password.encode())
        return encrypted_password.decode(), key.decode()

    def decrypt_password(self, encrypted_password, secret_key):
        fernet = Fernet(secret_key.encode())
        decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
        return decrypted_password

    def generate_user_id(self):
        while True:
            user_id = str(random.randint(100000, 999999))
            c.execute("SELECT user_id FROM patient WHERE user_id = ?",
                      (user_id,))
            if not c.fetchone():
                return user_id


    def send_sms(self, to_number, message_body):
        message = self.twilio_client.messages.create(
            body=message_body,
            from_=self.twilio_number,
            to=to_number
        )
        print(f"Sent message: {message.sid}")




app = Share()
app.main_menu()
