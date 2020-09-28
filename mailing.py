import os
import smtplib
from email.message import EmailMessage


def send_mail(mail, subject, content, attach_path):
    # email address and password stored in environment variables
    EMAIL_ADDRESS = os.environ.get('US_Email')
    EMAIL_PASSWORD = os.environ.get('US_pass')

    msg = EmailMessage()
    msg['Subject'] = str(subject)
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = str(mail)
    msg.set_content(content)

    if attach_path == 0:  # if attach_path = 0, no attachment is considered
        pass
    else:

        with open(attach_path, 'rb') as f:  # if attach_path is passed to function, it should be the path to attachment
            file_data = f.read()
            file_name = f.name
            file_type = "xlsx"

        msg.add_attachment(file_data, maintype="application", subtype=file_type, filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)


#send_mail('noclues008@gmail.com', 'Prompt about your stock', 'Stock price Hit')
