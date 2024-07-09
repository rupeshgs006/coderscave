# Share App

## Overview
The Share App is a Python-based application that allows users to manage administrative and patient records, including secure authentication, appointment management, and SMS notifications using the Twilio API. The app uses SQLite for data storage and the Cryptography library for secure password encryption.

## Features
- **Admin and Patient Authentication**: Secure login and signup for both admins and patients.
- **Password Encryption**: Encrypts and decrypts passwords using a secret key.
- **SMS Notifications**: Sends SMS notifications for login and appointment details using the Twilio API.
- **Appointment Management**: Admins and patients can add and view appointments.
- **Patient Management**: Admins can view patient details and list all patients.

## Prerequisites
- Python 3.7 or higher
- SQLite3
- Twilio account with an API key
- Required Python packages:
  - cryptography
  - twilio

## Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Required Packages**:
   ```bash
   pip install cryptography twilio
   ```

3. **Set Up Twilio Credentials**:
   - Replace `'account sid'`, `'auth token'`, and `'twilio number'` with your actual Twilio account SID, authentication token, and Twilio phone number in the `__init__` method of the `Share` class.

## Database Schema

- **Admin Table**:
  ```sql
  CREATE TABLE IF NOT EXISTS admin (
      user_id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      secret_key TEXT NOT NULL,
      encrypted_password TEXT NOT NULL,
      date_of_joining DATE NOT NULL,
      mobile_number TEXT
  );
  ```

- **Patient Table**:
  ```sql
  CREATE TABLE IF NOT EXISTS patient (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      user_id TEXT NOT NULL,
      secret_key TEXT NOT NULL,
      encrypted_password TEXT NOT NULL,
      mobile_number TEXT
  );
  ```

- **Appointments Table**:
  - This table is created dynamically for each patient and named as `user_<user_id>`.

## Running the Application
1. **Start the Application**:
   ```bash
   python <script_name>.py
   ```

2. **Main Menu**:
   - Choose between Admin and Patient functionalities or exit the application.

## Admin Functionalities

1. **Admin Signup**:
   - Enter name, password, mobile number, and date of joining.
   - A unique user ID is generated and saved in the database.
   - An SMS notification is sent to the admin's mobile number.

2. **Admin Login**:
   - Enter user ID and password.
   - If authenticated, the admin can perform operations such as viewing patients and patient details.

## Patient Functionalities

1. **Patient Signup**:
   - Enter name, password, and mobile number.
   - A unique user ID is generated and saved in the database.
   - An SMS notification is sent to the patient's mobile number.

2. **Patient Login**:
   - Enter user ID and password.
   - If authenticated, the patient can add and view appointments.

## Helper Functions

- **Password Encryption**:
  ```python
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
  ```

- **Password Decryption**:
  ```python
  def decrypt_password(self, encrypted_password, secret_key):
      fernet = Fernet(secret_key.encode())
      decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
      return decrypted_password
  ```

- **Generate User ID**:
  ```python
  def generate_user_id(self):
      while True:
          user_id = str(random.randint(100000, 999999))
          c.execute("SELECT user_id FROM patient WHERE user_id = ?", (user_id,))
          if not c.fetchone():
              return user_id
  ```

- **Send SMS**:
  ```python
  def send_sms(self, to_number, message_body):
      message = self.twilio_client.messages.create(
          body=message_body,
          from_=self.twilio_number,
          to=to_number
      )
      print(f"Sent message: {message.sid}")
  ```

## Note
- Make sure to replace placeholder values with actual credentials and configurations.
- Ensure that the SQLite database and necessary tables are properly set up before running the application.
