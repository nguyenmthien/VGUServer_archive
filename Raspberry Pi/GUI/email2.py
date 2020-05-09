import os
import sys, ssl, email

from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
from dotenv import load_dotenv
load_dotenv()
SMTP_Host = 'smtp.gmail.com'
MY_ADDRESS = os.getenv('ADDRESS')
PASSWORD = os.getenv('P_W')

def get_contacts(filename):
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for contact in contacts_file:
            emails = contact.split()
    return emails

def send_email_file(filename):
    
    emails = get_contacts(filename)
    print(emails)

    s = SMTP(host=SMTP_Host, port=465)
    s.login(MY_ADDRESS, PASSWORD)

    ex_temp = 26
    ex_humid = 65

    text_subtype = 'plain' # typical values for text_subtype are plain, html, xml
    content = """\
    The temperature is {temp}°C and the humidity is {humid}%.
    """
    subject = "Hi! This is your information for VGU Server"

    try:
        for email in emails:
            msg = MIMEMultipart()
            msg['From'] = MY_ADDRESS
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(content.format(temp=ex_temp,humid=ex_humid), text_subtype))
            #msg.attach(MIMEText(html, 'html'))
            s.send_message(msg)
            del msg
    except:
        pass

    s.quit()

def send_email_list(emails, filename):
    #emails = list
    #filename = 'contacts.txt'

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Establish a connection with Gmail’s SMTP server, then login with email address and password
    s = SMTP(host=SMTP_Host, port=465, context=context)
    s.login(MY_ADDRESS, PASSWORD)

    text_subtype = 'plain' # typical values for text_subtype are plain, html, xml
    content = """\
    Your data is stored in the attachment below
    """
    subject = "Hi! This is your information for VGU Server"

    #Open CSV file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email 
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    try:
        for a_email in emails:
            # Create a multipart message and set headers
            msg = MIMEMultipart()
            msg['From'] = MY_ADDRESS
            msg['To'] = a_email
            msg['Subject'] = subject
            # Add body to email
            msg.attach(MIMEText(content, text_subtype))
            # Add attachment to message and convert message to string
            msg.attach(part)
            text = msg.as_string()
            s.sendmail(MY_ADDRESS, a_email, text)
            del msg
    except:
        pass

    s.quit()
