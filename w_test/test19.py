from bs4 import BeautifulSoup

import errors
from fail_pass import failed, passed
from general_functions import get_course_dict, get_course_id


def test19(url_class):
    first_name = "test"
    last_name = "20"
    username = "test19"
    password = "OlDpishExcel18"
    data = dict(first_name=first_name, last_name=last_name, username=username, email="test19@gmail.com", password1=password,
                password2=password)

    url_class.reg_and_log(data)
    url = url_class.get_courses_urls()
    client = url_class.client
    courses_data = [get_course_dict(exam_date="1398-08-17"), get_course_dict(exam_date="1398-08-17"),
                    get_course_dict(exam_date="1092-04-20")]

    for i in courses_data:
        url_class.make_course(i)

    page = client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    for c in courses_data:
        url_class.add_course(soup, c)

    page = url_class.client.get(url_class.get_courses_urls())
    soup = BeautifulSoup(page.content, 'html.parser')
    my_div = soup.find('div', id='my_courses')

    for course in courses_data[0:2]:
        course_div = my_div.find(lambda tag: tag.name == "div" and tag.get('class')and
                                                   get_course_id(course) in tag.get('class'))
        errors_ = course_div.find_all(lambda tag: tag.name == "span" and tag.get('class')and "error" in tag.get('class'))
        ok = False
        for error_text in errors_:
            ok = ok or (error_text and error_text.getText().__contains__('زمان امتحان درس با سایر امتحان‌ها تداخل دارد'))
        if not ok:
            return failed('test19', errors.fail_to_show_error)

    course_div = my_div.find(lambda tag: tag.name == "div" and tag.get('class')and get_course_id(courses_data[2])
                                         in tag.get('class'))
    errors_ = course_div.find_all(lambda tag: tag.name == "span" and tag.get('class')and "error" in tag.get('class'))
    for error_text in errors_:
        if error_text and error_text.getText().__contains__('زمان امتحان درس با سایر امتحان‌ها تداخل دارد'):
            return failed('test19', errors.show_incorrect_error)

    return passed("test19")

