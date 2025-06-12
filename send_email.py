import smtplib, os
from datetime import datetime
from zoneinfo import ZoneInfo
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# Email configuration
SMTP_SERVER = os.getenv("EMAIL_HOST")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
SMTP_PORT = os.getenv("PORT")

def send_email(recipient_email, subject, body, body_type):
    """
    Uses my Gmail send an email to a recipient.
    
    Parameters:
        recipient_email (str): A recipient email
        subject (str): An email subject.
        body (str): An email body.
        body_type (str): A type of email body, plain / html.
    """

    try:
        # Create the email message
        e_msg = MIMEMultipart()
        e_msg["Subject"] = subject
        e_msg["From"] = SENDER_EMAIL
        e_msg["To"] = recipient_email

        e_msg.attach(MIMEText(body, body_type))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, e_msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    bkk_tz = ZoneInfo('Asia/Bangkok')
    date_time = datetime.now(bkk_tz).strftime("%d %b %Y %H:%M:%S")
    stock = "MDX"
    stock_price = str(3.5)

    email_recipient = "porla113@gmail.com"
    email_subject = "Stock Price Alert!"
    email_body = f"On {date_time}, <b>{stock}</b> price is <b>{stock_price}</b>!"
    email_body_type = "html"

    send_email(email_recipient, email_subject, email_body, email_body_type)