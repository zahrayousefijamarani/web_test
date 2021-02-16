from bs4 import BeautifulSoup

import errors
from fail_pass import failed, passed
from general_functions import get_course_dict, get_course_id
from urls import  validate_url
import string
import random


def random_generator(size=6, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for x in range(size))


def test22(url_class):
    first_name = "test"
    last_name = "23"
    username = "test22"
    password = "OlDpishExcel18"
    data = dict(first_name=first_name, last_name=last_name, username=username, email="test22@gmail.com",
                password1=password,
                password2=password)

    url_class.reg_and_log(data)

    course_page_url = url_class.get_courses_urls()
    client = url_class.client
    course_data = get_course_dict()
    url_class.make_course(course_data)

    page = client.get(course_page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_div = soup.find('div', id='all_courses')

    div = all_div.find(
        lambda tag: tag.name == "div" and tag.get('class')and get_course_id(course_data) in tag.get('class'))

    details_link = div.find(lambda tag: tag.name == "a" and tag.get('class')and 'details' in tag.get('class'))

    course_page_url = validate_url(url_class.base_url, details_link['href'])
    page = url_class.client.get(course_page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    comment_div = soup.find('div', id='comments')
    if not comment_div:
        return failed('test22', errors.comment_div_error)
    comment_form = comment_div.find('form', id='comment_form')
    if not comment_form:
        return failed('test22', errors.comment_form_error)

    inputs = comment_form.find_all('textarea')
    if not inputs:
        return failed("test22", errors.fields_not_found)
    tag_names = set([tag.get('name') for tag in inputs])

    required_names = {'comment'}
    if not required_names.issubset(tag_names):
        return failed("test22", errors.fields_not_found)

    comment_text = random_generator(10)
    data = dict(comment=comment_text)
    page = url_class.send_form(course_page_url, "comment_form", data)
    if page.status_code != 200:
        return failed('test22', errors.fail_to_comment)

    page = url_class.client.get(course_page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    comment_div = soup.find('div', id='comments')
    comment_div_divs = comment_div.find_all('div')
    for div in comment_div_divs:
        # text = div.find(lambda tag: tag.name == "p" and tag.get('class')and "text" in tag.get('class'))
        # if text and text.getText().__contains__(comment_text):
        #     return passed('test22')
        text = div.find(lambda tag: tag.name == "p" and tag.get('class')and "text" in tag.get('class'))
        title = div.find(lambda tag: tag.name == "span" and tag.get('class')and "name" in tag.get('class'))
        if text and text.getText().__contains__(comment_text) and title and title.getText().__contains__(first_name)\
                and title.getText().__contains__(last_name):
            return passed('test22')

    return failed('test22', errors.comment_failed)
