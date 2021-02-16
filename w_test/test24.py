from bs4 import BeautifulSoup

import errors
from fail_pass import failed, passed
from general_functions import get_course_dict, get_course_id
from urls import  validate_url
import random


def test24(url_class):
    number = 0

    first_name = "test"
    last_name = "25"
    username = "test24"
    password = "OlDpishExcel18"
    data = dict(first_name=first_name, last_name=last_name, username=username, email="test24@gmail.com", password1=password,
                password2=password)

    url_class.reg_and_log(data)

    url = url_class.get_courses_urls()
    client = url_class.client
    course_data = get_course_dict()

    url_class.make_course(course_data)

    for i in range(random.randint(5, 15)):
        user_data = dict(first_name="saba", last_name="h", username="test24_user" + str(i),
                         email="test24" + str(i) + "@gmail.com",
                    password1=password,
                    password2=password)

        url_class.reg_and_log(user_data)
        page = client.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        url_class.add_course(soup, course_data)
        number += 1

    all_div = soup.find('div', id='all_courses')
    first_div = all_div.find(lambda tag: tag.name == "div" and tag.get('class')and get_course_id(course_data) in tag.get('class'))
    first_detail_link = first_div.find(lambda tag: tag.name == "a" and tag.get('class')and "details" in tag.get('class'))
    course_page_url = validate_url(url_class.base_url, first_detail_link['href'])
    page = url_class.client.get(course_page_url)

    soup = BeautifulSoup(page.content, 'html.parser')
    student_number = soup.find('p', id='students_count')
    if not student_number:
        return failed('test24', errors.student_number_paragraph)
    if not student_number.getText().__contains__(str(number)):
        return failed('test24', errors.student_number_error)

    return passed('test24')
