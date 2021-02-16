import requests
from bs4 import BeautifulSoup

import errors
from errors import contact_us_link_error, form_div_error
from fail_pass import failed, passed


def check_next_page(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify()[:7000])
    done = soup.find('div', id="done")
    if done and done.getText().__contains__('درخواست شما ثبت شد'):
        return True


def check_this_page(url_class, page):
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify()[:6000])
    # print(page.url)
    # print(url_class.get_contact_us_url())
    if page.url == url_class.get_contact_us_url() or page.url == url_class.get_contact_us_url() + "/":
        return True
    return False


def test5(url_class):
    url = url_class.get_contact_us_url()
    if not url:
        return failed("test5", contact_us_link_error)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    form = soup.find('form', id="contact_us_form")
    if not form:
        return failed("test5", form_div_error)

    inputs = form.find_all('input')
    if not inputs:
        return failed("test2", errors.fields_not_found)
    tag_names = set([tag.get('name') for tag in inputs])
    text_area = form.find('textarea')

    required_names = {'title', 'email'}

    if not required_names.issubset(tag_names) or not text_area or text_area.get('name') != 'text':
        return failed("test5", errors.fields_not_found)

    client = url_class.client

    data = dict(title='test5', text='123456789012s', email="test5_1@gmail.com")
    data2 = dict(title='test5', text='1212s', email="test5_2@gmail.com")

    page = url_class.send_form(url, "contact_us_form", data)

    if check_next_page(page):
        page = url_class.send_form(url, "contact_us_form", data2)
        if check_this_page(url_class, page):
            return passed('test5')
        else:
            return failed('test5', errors.text_error)

    return failed('test5', errors.message_not_send)
