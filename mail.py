import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import Files

sender_server = files.read_config('Mail', 'Sender_Server')
sender_account = files.read_config('Mail', 'Sender_Account')
sender_password = files.read_config('Mail', 'Sender_Password')
sender_name = files.read_config('Mail', 'Sender_Name')
receiver_account = files.read_config('Mail', 'Receiver_Account')
receiver_name = files.read_config('Mail', 'Receiver_Name')

def content_config(subject, content):
    message = MIMEMultipart()
    message.attach(MIMEText(content, 'html', 'utf-8'))
    message['Subject'] = subject
    message['From'] = sender_name+'<'+sender_account+'>'
    message['To'] = receiver_name
    return message


def content_generator(title, mail_type, content, link_name, link):
    with open('mail.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    html_content = html_content.replace('|Title of Notification|', title)
    html_content = html_content.replace('|Type of Notification|', mail_type)
    html_content = html_content.replace('|Content of Notification|', content)
    html_content = html_content.replace('|Link of Notification|', link)
    html_content = html_content.replace('|Name of Link|', link_name)
    return html_content


def send_html_mail(message):
    try:
        smtp_object = smtplib.SMTP_SSL(sender_server)
        smtp_object.login(sender_account, sender_password)
        smtp_object.sendmail(sender_account, receiver_account, message.as_string())
        smtp_object.quit()
        print('Mail sent successfully')
    except smtplib.SMTPException as e:
        print(e)

