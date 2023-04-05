import yagmail
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('LECTUREBOOST_EMAIL')
app_password = os.getenv('EMAIL_PASSWORD')
SUBJECT = 'Your Lecture Links'

def send_links(links, to):
    content = ['Here\'s the links to your enhanced lecture contents: ']
    for link in links: content.append(link)

    with yagmail.SMTP(user, app_password) as yag:
        yag.send(to, SUBJECT, content)
        print('Sent email successfully')