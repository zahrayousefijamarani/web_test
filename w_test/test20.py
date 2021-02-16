from bs4 import BeautifulSoup

import errors
from fail_pass import failed, passed
from general_functions import get_course_dict, get_course_id


def test20(url_class):
    first_name = "test"
    last_name = "21"
    username = "test20"
    password = "OlDpishExcel18"
    data = dict(first_name=first_name, last_name=last_name, username=username, email="test20@gmail.com",
                password1=password,
                password2=password)

    url_class.reg_and_log(data)

    courses_data = [get_course_dict(start_time="14:00", end_time="16:00"),
                    get_course_dict(start_time="14:30", end_time="17:30"),
                    get_course_dict(start_time="14:00", end_time="16:00"),
                    get_course_dict(start_time="14:30", end_time="15:30"),
                    get_course_dict(start_time="00:00", end_time="00:10")]

    url = url_class.get_courses_urls()
    client = url_class.client
    for i in courses_data:
        url_class.make_course(i)

    page = client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    for c in courses_data:
        url_class.add_course(soup, c)

    page = client.get(url_class.get_courses_urls())
    soup = BeautifulSoup(page.content, 'html.parser')
    my_div = soup.find('div', id='my_courses')

    for course in courses_data[0:4]:
        course_div = my_div.find(
            lambda tag: tag.name == "div" and tag.get('class')and get_course_id(course) in tag.get('class'))
        if not course_div:
            return failed('test20', errors.course_not_found_in_my_courses)

        errors_ = course_div.find_all(
            lambda tag: tag.name == "span" and tag.get('class')and "error" in tag.get('class'))
        ok = False
        for error_text in errors_:
            ok = ok or (error_text and error_text.getText().__contains__('زمان درس با سایر دروس تداخل دارد'))

        if not ok:
            return failed('test20', errors.fail_to_show_error)

    for course in courses_data[4:]:
        course_div = my_div.find(
            lambda tag: tag.name == "div" and tag.get('class')and get_course_id(course) in tag.get('class'))
        if not course_div:
            return failed('test20', errors.course_not_found_in_my_courses)

        errors_ = course_div.find_all(
            lambda tag: tag.name == "span" and tag.get('class')and "error" in tag.get('class'))

        for error_text in errors_:
            if error_text and error_text.getText().__contains__('زمان درس با سایر دروس تداخل دارد'):
                return failed("test20", errors.show_incorrect_error)

    return passed("test20")
