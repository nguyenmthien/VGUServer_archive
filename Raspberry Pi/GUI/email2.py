import sys
from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
# from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from string import Template

SMTP_Host = 'smtp.gmail.com'
MY_ADDRESS = 'spam.team1.groupcd.ee4.vgu@gmail.com'
PASSWORD = "H376r923l84b"

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

def send_email_list(list):
    emails = list

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
