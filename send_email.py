import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# Email configuration
SMTP_SERVER = os.getenv("EMAIL_HOST")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
SMTP_PORT = os.getenv("PORT")

def send_email(recipient_email, subject, body):

    try:
        # Create the email message
        e_msg = MIMEMultipart()
        e_msg["Subject"] = subject
        e_msg["From"] = SENDER_EMAIL
        e_msg["To"] = recipient_email

        e_msg.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, e_msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")