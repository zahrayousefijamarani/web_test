import requests
from bs4 import BeautifulSoup

from errors import login_link_error, form_div_error, fields_not_found, login_failed, fail_to_show_error, error_div_error
from fail_pass import failed, passed


def check_login(url_class, page):
    soup = BeautifulSoup(page.content, 'html.parser')
    navbar = soup.find('div', id="navbar")
    link = navbar.find("a", id='logout')
    if not link or (page.url != url_class.get_home_url() and page.url == url_class.get_home_url() + "/"):
        return False
    link = navbar.find("a", id='login')
    if not link:
        return True
    return False


def check_not_login(url_class, page):
    soup = BeautifulSoup(page.content, 'html.parser')
    error = soup.find('div', id="errors")
    if not error:
        return failed("test4", error_div_error)
    navbar = soup.find('div', id="navbar")
    link = navbar.find("a", id='login')
    if not link or (page.url != url_class.get_login_url() and page.url == url_class.get_login_url() + "/"):
        return False
    link = navbar.find("a", id='logout')
    if not link:
        return True

    return False


def test3(url_class):
    username = "test3"
    password = "OlDpishExcel18&#"
    wrong_username = username + "1"
    wrong_password = password + "1"
    data = dict(first_name="saba", last_name="h", username=username, email="test3@gmail.com", password1=password,
                password2=password)

    url = url_class.get_register_url()
    url_class.register(url, data)

    url = url_class.get_login_url()
    if not url:
        return failed("test3", login_link_error)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    form = soup.find('form', id="login_form")
    if not form:
        return failed("test3", form_div_error)

    inputs = form.find_all('input')
    if not inputs:
        return failed("test2", fields_not_found)
    tag_names = set([tag.get('name') for tag in inputs])

    required_names = {'username', 'password'}

    if not required_names.issubset(tag_names):
        return failed("test3", fields_not_found)

    client = url_class.client

    data = dict(username=username, password=password)
    data2 = dict(username=wrong_username, password=password)
    data3 = dict(username=username, password=wrong_password)

    page = url_class.send_form(url, "login_form", data2)

    if not check_not_login(url_class, page):  # "login with wrong username!"
        return failed("test3", login_failed)

    page = url_class.send_form(url, "login_form", data3)

    if not check_not_login(url_class, page):  # "login with wrong password!"
        return failed("test3", login_failed)

    page = url_class.send_form(url, "login_form", data)

    if not check_login(url_class, page):
        return failed("test3", login_failed)

    return passed("test3")

