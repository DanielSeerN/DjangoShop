from dotenv import load_dotenv

import os
import smtplib

load_dotenv()
EMAIL = os.getenv('email_host_user')
PASSWORD = os.getenv('email_host_password')


def send_notification_email(user_email):
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, f'{user_email}', 'Здравствуйте! Мы получили ваше сообщение.')
    server.quit()


def send_email_to_host(user_email, email_text):
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, EMAIL, f'{email_text} от {user_email}')
    server.quit()
