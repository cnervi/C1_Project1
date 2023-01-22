import smtplib
import ssl
from schedule import every, run_pending
import time
import csv

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_emails():
    subject = "Daily Report"
    body = "This is an email with a daily report."
    sender_email = input("Email: ")  # Temporary solution so everyone can use it
    password = input("password: ")  # Temporary solution so everyone can use it
    recipients = ["myemail@gmail.com", "myemail@gmail.com", "myemail@gmail.com"]

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["Subject"] = subject
    message["To"] = "".join(recipients)

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    filename = "report.pdf"

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header("Content-Disposition", f"attachment; filename= {filename}", )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    # Using localhost and port 1025(change to "smtp.gmail.com,465" for gmail)
    with smtplib.SMTP_SSL("smtp.localhost", 1025, context=context) as server:
        server.login(sender_email, password)
        # For each recipient send an email and write the email adress and its subject
        for i in range(len(recipients)):
            try:
                server.sendmail(sender_email, recipients[i], text)
                with open("emails_sent.csv", 'w') as f:
                    # create the csv writer
                    writer = csv.writer(f)
                    # write a row to the csv file
                    writer.writerow((recipients[i], subject))
            except Exception as e:
                # For each error write email adress and an error
                with open("errors.csv", 'w') as f:
                    writer = csv.writer(f)
                    writer.writerow((recipients[i], str(e)))
                    print(e)
            finally:
                server.quit()


every().day.at("08:00").do(send_emails())
while True:
    run_pending()
    time.sleep(1)
