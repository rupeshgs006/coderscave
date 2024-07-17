import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email account credentials
sender_email = "example@hotmail.com"
sender_password = "Enter your password"  

# Read recipient emails from CSV file
csv_file = 'recipients.csv'

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["Subject"] = "Enter the subject"

# Add body to email
body = "Hello, this is the body of the email."
message.attach(MIMEText(body, "plain"))

# SMTP server configuration for Outlook (hotmail.com)
smtp_server = "smtp-mail.outlook.com"
smtp_port = 587

try:
    # Create a secure SSL context
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        
        # Read recipients from CSV file
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                recipient_email = row['email']
                message["To"] = recipient_email
                server.sendmail(sender_email, recipient_email, message.as_string())
                print(f"Email sent successfully to {recipient_email}")
                
    print("All emails sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
