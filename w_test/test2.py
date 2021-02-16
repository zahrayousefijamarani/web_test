import requests
from bs4 import BeautifulSoup

from errors import user_not_found_in_db, register_link_error, form_div_error, fields_not_found, \
    register_error, submit_button_not_found, redirect_failed
from fail_pass import failed, passed
from urls import  validate_url


def check_user_in_admin_page(url_class,username):
    page = url_class.login_as_admin()
    if page.status_code != 200:
        return failed("test2", "Admin page not found")
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find("div", id="content")
    links = div.find_all(lambda tag: tag.name == "a")

    for link in links:
        users_url = validate_url(url_class.base_url, link['href'])
        users_page = url_class.client.get(users_url)
        soup = BeautifulSoup(users_page.content, 'html.parser')
        username_links = soup.find_all(lambda tag: tag.getText().__contains__(username))
        if username_links:
            return passed("test2")

    return failed("test2", user_not_found_in_db)


def test2(url_class):
    url = url_class.get_register_url()
    if not url:
        return failed("test2", register_link_error)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    form = soup.find('form', id="register_form")
    if not form:
        return failed("test2", form_div_error)

    inputs = form.find_all('input')
    if not inputs:
        return failed("test2", fields_not_found)
    tag_names = set([tag.get('name') for tag in inputs])

    required_names = {'first_name', 'last_name', 'username', 'email', 'password1', 'password2'}

    if not required_names.issubset(tag_names):
        return failed("test2", fields_not_found)

    buttons = form.find("button", attrs={'name': "submit"})
    if not buttons:
        return failed("test2", submit_button_not_found)

    username = "test20234"
    data = dict(first_name="saba", last_name="h", username=username, email="test2@gmail.com", password1="OlDpishExcel18&#",
                password2="OlDpishExcel18&#")

    page = url_class.send_form(url, "register_form", data)
    if page.status_code != 200:
        return failed("test2", register_error)

    return check_user_in_admin_page(url_class, username)
