import email
import imaplib
import random
import string
import time

import requests

from errors import mail_server_error, mail_title_incorrect, mail_content_incorrect
from fail_pass import failed, passed

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "webe19lopers" + ORG_EMAIL
FROM_PWD = "fK5-f8L-Luf-ZX5"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993
encoding = 'utf-8'


def send_contact_us_message(url_class,title, text, form_email):
    url = url_class.get_contact_us_url()
    data = dict(title=title, text=text, email=form_email)
    page = url_class.send_form(url, "contact_us_form", data)


def check_if_mail_received(form_subject, form_text, form_email):

    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    try:
        mail.login(FROM_EMAIL, FROM_PWD)
    except imaplib.IMAP4.error:
        return failed("test6", mail_server_error)

    mail.select('inbox')
    result, data = mail.search(None, "ALL")
    mail_ids = data[0]
    id_list = mail_ids.split()

    subject_found = False
    text_found = False
    email_found = False

    for mail_id in id_list:
        result, data = mail.fetch(mail_id, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email.decode(encoding))
        title = email_message['Subject']
        text = email_message.get_payload(decode=True)

        if title and title.__contains__(form_subject):
            subject_found = True
            if text and text.decode(encoding).__contains__(form_text):
                text_found = True
                if text.decode(encoding).__contains__(form_email):
                    email_found = True

    if not subject_found:
        return failed("test6", mail_title_incorrect)
    if not text_found or not email_found:
        return failed("test6", mail_content_incorrect)
    return passed("test6")


def random_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def test6(url_class):
    title = random_generator(10)
    text = random_generator(100)
    form_email = "test6@gmail.com"

    send_contact_us_message(url_class, title, text, form_email)
    time.sleep(2.5)
    return check_if_mail_received(title, text, form_email)
