import requests
from bs4 import BeautifulSoup

from urls import base_url


def go_admin_page():
    username = 'admin'
    password = 'admin123456'
    # url = base_url + "admin/login/?next=/admin/"
    url = "http://127.0.0.1:8000/admin/login/?next=/admin/"
    client = requests.session()
    csrf = client.get(url).cookies['csrftoken']
    data = dict(username='ali', password='zahra12345', csrfmiddlewaretoken=csrf)
    # data = dict(username=username, password=password, csrfmiddlewaretoken=csrf)
    page = client.post(url, data=data, headers=dict(Referer=url))

    check_course(dict(), page)


def check_course(dic, page):
    soup = BeautifulSoup(page.content, 'html.parser')
    model_div = soup.find('tr', {'class': 'model-person'})
    # model_div = soup.find('tr', {'class': 'model-course'})
    child = model_div.findChildren("th", recursive=False)
    # course_link = str(child).split('href="')[1].split('">Courses</a>')[0]
    course_link = str(child).split('href="/')[1].split('">Persons</a>')[0]
    # url = base_url + course_link
    url = "http://127.0.0.1:8000/" + course_link
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    change_list = soup.find('div', id='changelist')
    print(change_list)
    result = change_list.findChildren("div", class_='result', recursive=False)

    print(result)
    # todo check course here


go_admin_page()
