import requests
from bs4 import BeautifulSoup
import shutil


def post_get():
    # headers_Get = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #     'Accept-Language': 'en-US,en;q=0.5',
    #     'Accept-Encoding': 'gzip, deflate',
    #     'DNT': '1',
    #     'Connection': 'keep-alive',
    #     'Upgrade-Insecure-Requests': '1'
    # }
    # q = "wwwwwwwww"
    # s = requests.Session()
    # q = '+'.join(q.split())
    # url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
    # r = s.get(url, headers=headers_Get)

    payload = {'key1': 'value1', 'key2': 'value2'}
    r = requests.get('http://httpbin.org', params=payload)
    soup = BeautifulSoup(r.content, 'html.parser')

    print(soup.prettify())
    print(r.url)

post_get()

def img1():
    url = "http://s7.picofile.com/file/8376132150/a80bb7891485ea0f4e34894663cb5bb0.jpg"
    response = requests.get(url, stream=True)
    with open('profile_image2.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    if open("profile_image.jpg", "rb").read() == open("profile_image2.jpg", "rb").read():
        print("yes")


def up1():
    url = "https://www.filedropper.com"

    client = requests.session()
    # csrf = client.get(url).cookies['csrftoken']
    files = {'file': open("profile_image.jpg", "rb")}
    print(files)
    page = client.post(url, files=files, timeout=None)

    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup.string)
    url = url + soup.string
    print(url)

    #
    # url = "https://encodable.com/uploaddemo/?action=listfiles"
    #
    # page = client.get(url)
    # soup = BeautifulSoup(page.content, 'html.parser')
    # cont = soup.find_all(lambda tag: tag.name == "tr" and tag.get("class") is not None and tag.get("class").__contains__("filerow"))
    # print(cont[0], sep="\n\n")
    # print(page.status_code)


def f4():  # in ok e ok e

    # with requests.Session() as session:
    username = "bbb"
    password = "1bbb234567"
    url2 = "http://btwitter.pythonanywhere.com/login/"
    client = requests.session()
    csrf = client.get(url2).cookies['csrftoken']
    data = dict(username=username, password=password, csrfmiddlewaretoken=csrf)

    page = client.post(url2, data=data, headers=dict(Referer=url2))
    soup = BeautifulSoup(page.content, 'html.parser')
    print(page.status_code)
    print(soup)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    url = "http://btwitter.pythonanywhere.com/new/"
    csrf = client.get(url).cookies['csrftoken']
    data = dict(content="happy new day", parent_tweet="9", csrfmiddlewaretoken=csrf)
    page = client.post(url, data=data, headers=dict(Referer=url))
    soup = BeautifulSoup(page.content, 'html.parser')
    print(page.status_code)
    print(soup)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    url = "http://btwitter.pythonanywhere.com/"
    # csrf = client.get(url).cookies['csrftoken']  # >>> in csrf begiri mimire
    data = dict(content="happy new day", parent_tweet="9", csrfmiddlewaretoken=csrf)
    page = client.get(url, headers=dict(Referer=url))
    soup = BeautifulSoup(page.content, 'html.parser')
    print(page.status_code)
    print(soup)


def f3():  # ok but not logged in
    username = "bbb"
    password= "1bbb234567"
    url2 = "http://btwitter.pythonanywhere.com/login/"
    client = requests.session()
    csrf = client.get("http://btwitter.pythonanywhere.com/login/").cookies['csrftoken']
    data = dict(username=username, password=password, csrfmiddlewaretoken=csrf)

    page = client.post(url2, data=data, headers=dict(Referer=url2))
    soup = BeautifulSoup(page.content, 'html.parser')
    print(page.status_code)
    print(soup)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    url = "http://btwitter.pythonanywhere.com/new/"
    client = requests.session()
    # csrf = client.get("http://btwitter.pythonanywhere.com/").cookies['csrftoken']
    data = dict(content="hey this is python")
    page = client.get(url, headers=dict(Referer=url))
    soup = BeautifulSoup(page.content, 'html.parser')
    print(page.status_code)
    print(soup)


def f1():
    url = "http://btwitter.pythonanywhere.com/signup/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    first_name_tag = soup.find('p', id="text_first_name")

    client = requests.session()
    csrf = client.get(url).cookies['csrftoken']
    username = "bbb"
    password= "1bbb234567"
    data = dict(username=username, password1=password, password2=password, csrfmiddlewaretoken=csrf)
    page = client.post(url, data=data, headers=dict(Referer=url))

    soup = BeautifulSoup(page.content, 'html.parser')

    print(page.status_code)
    print(soup)

    url2 = "http://btwitter.pythonanywhere.com/login/"
    data = dict(username=username, password=password, csrfmiddlewaretoken=csrf)
    page = client.post(url2, data=data, headers=dict(Referer=url))
    print(page.status_code)
    print(soup)

    url3 = "http://btwitter.pythonanywhere.com/new/"
    data = dict(content="hey this is python", csrfmiddlewaretoken=csrf)
    page = client.post(url3, data=data, headers=dict(Referer=url))
    print(page.status_code)
    print(soup)


def f2():
    url0 = "http://btwitter.pythonanywhere.com/"

    url = "http://btwitter.pythonanywhere.com/signup/"
    url2 = "http://btwitter.pythonanywhere.com/login/"
    url3 = "http://btwitter.pythonanywhere.com/new/"
    #
    # client = requests.session()
    # csrf = client.get(url0).cookies['csrftoken']

    username = "bbb"
    password = "1bbb234567"

    with requests.Session() as session:
        # csrf = session.get(url0).cookies['csrftoken']
        client = requests.session()
        csrf = client.get(url0).cookies['csrftoken']
        payload = dict(username=username, password=password, csrfmiddlewaretoken=csrf)

        post = session.post(url2, data=payload)
        print(post.content)
        data = dict(content="hey this is python", csrfmiddlewaretoken=csrf)

        # page = session.post(url3, data=data)
        # soup = BeautifulSoup(page.content, 'html.parser')
        # print(page.status_code)
        # print(soup)




# a = "salam saba chetori"
# b = "aba"
# if a.__contains__(b):
#     print("yes")


# s = b"=?utf-8?B?2LPZhNin2YUg2KjbjNi02KrYsQ==?=".decode()
#
# print(s)
#
# w = "سلام بیشتر".encode('UTF_8')
#
# print(w)
#
# t = b'\xd8\xb3\xd9\x84\xd8\xa7\xd9\x85 \xd8\xa8\xdb\x8c\xd8\xb4\xd8\xaa\xd8\xb1'.decode()
#
# print(t)
#
# g = b"2LPZhNin2YUg2KjbjNi02KrYsQ==".decode()
# print(g)


# def read_email_from_gmail():
#     try:
#         mail = imaplib.IMAP4_SSL(SMTP_SERVER)
#         mail.login(FROM_EMAIL,FROM_PWD)
#         mail.select('inbox')
#
#         typ, data = mail.search(None, 'ALL')
#         mail_ids = data[0]
#
#         id_list = mail_ids.split()
#         first_email_id = int(id_list[0])
#         latest_email_id = int(id_list[-1])
#
#
#         for i in range(latest_email_id,first_email_id, -1):
#             typ, data = mail.fetch(i, '(RFC822)' )
#
#             for response_part in data:
#                 if isinstance(response_part, tuple):
#                     msg = email.message_from_string(response_part[1])
#                     email_subject = msg['subject']
#                     email_from = msg['from']
#                     print( 'From : ' + email_from + '\n')
#                     print ('Subject : ' + email_subject + '\n')
#
#     except Exception, e:
#         print str(e)

#
# client = requests.session()
# # Retrieve the CSRF token first
# csrf = client.get(url).cookies['csrftoken']
#
#
# data = dict(username="bb", password1="1bb234567", ipassword2="1bb234567", csrfmiddlewaretoken=csrf)
# page = client.post(url, data=data, headers=dict(Referer=url))
#
#
# soup = BeautifulSoup(page.content, 'html.parser')
#
# print(page.status_code)
# print(page)
# print(soup)
#
# import requests
#


# page = requests.get(url)
# soup = BeautifulSoup(page.content, 'html.parser')
# tag = soup.find_all('a', href="/signup/")
# print(type(tag))
#
# tag = soup.find('a', href="/signup/")
# print(tag.get('href'))
#
# if tag:
#     print(tag.get('href'))
# else:
#     print("no")



