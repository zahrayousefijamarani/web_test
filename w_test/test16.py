from bs4 import BeautifulSoup

import errors

from fail_pass import failed, passed
from general_functions import get_course_dict, get_course_id
from urls import validate_url


def test16(url_class):
    first_name = "test"
    last_name = "17"
    username = "test16"
    password = "OlDpishExcel18"
    data = dict(first_name=first_name, last_name=last_name, username=username, email="test16@gmail.com",
                password1=password,
                password2=password)

    url_class.reg_and_log(data)

    url = url_class.get_courses_urls()
    if not url:
        return failed("test16", errors.courses_link_error)

    courses_data = [get_course_dict(), get_course_dict()]

    for i in courses_data:
        url_class.make_course(i)

    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())
    all_div = soup.find('div', id='all_courses')
    if not all_div:
        return failed('test16', errors.all_course_div_error)

    first_div = all_div.find(
        lambda tag: tag.name == "div" and tag.get('class')and get_course_id(courses_data[0]) in tag.get('class'))
    if not first_div:
        return failed('test16', errors.course_box_error)
    second_div = all_div.find(
        lambda tag: tag.name == "div" and tag.get('class')and get_course_id(courses_data[1]) in tag.get('class'))
    if not second_div:
        return failed('test16', errors.course_box_error)

    first_add_link = first_div.find(lambda tag: tag.name == "a" and tag.get('class')and 'add' in tag.get('class'))
    if not first_add_link:
        return failed('test16', errors.add_link_error)
    second_add_link = second_div.find(lambda tag: tag.name == "a" and tag.get('class')and 'add' in tag.get('class'))
    if not second_add_link:
        return failed('test16', errors.add_link_error)

    page = url_class.client.get(validate_url(url, first_add_link['href']))
    soup = BeautifulSoup(page.content, 'html.parser')
    if page.status_code != 200:
        return failed('test16', errors.fail_to_get_course)

    page = url_class.client.get(url_class.get_courses_urls())
    soup = BeautifulSoup(page.content, 'html.parser')
    my_div = soup.find('div', id='my_courses')
    if not my_div:
        return failed('test16', errors.my_courses_div_error)
    first_course_div = my_div.find(
        lambda tag: tag.name == "div" and tag.get('class')and get_course_id(courses_data[0]) in tag.get('class'))
    if not first_course_div:
        return failed('test16', errors.course_not_found_in_my_courses)

    all_div = soup.find('div', id='all_courses')
    first__taken_div = all_div.find(
        lambda tag: tag.name == "div" and tag.get('class')and get_course_id(courses_data[0]) in tag.get('class'))
    if first__taken_div:
        return failed('test16', errors.taken_course_found)
    second_not_taken_div = all_div.find(
        lambda tag: tag.name == "div" and tag.get('class')and get_course_id(courses_data[1]) in tag.get('class'))
    if not second_not_taken_div:
        return failed('test16', errors.course_box_error)

    return passed("test16")
