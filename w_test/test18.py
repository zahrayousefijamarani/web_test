from bs4 import BeautifulSoup

import errors
from errors import form_div_error, fields_not_found, make_new_course_link_error
from fail_pass import failed
from general_functions import get_course_dict
from test11_2 import test11_1


def test18(url_class):
    url_class.login_as_admin()

    url = url_class.get_new_course_url()

    if not url:
        return failed("test18", make_new_course_link_error)  # error for test 11

    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    form = soup.find('form', id="make_course")
    if not form:
        return failed("test18", form_div_error)

    inputs = form.find_all('input') + form.find_all('select')
    tag_names = set([tag.get('name') for tag in inputs])

    required_names = {'department', 'name', 'group_number', 'course_number', 'teacher', 'start_time', 'end_time',
                      'first_day', 'second_day', 'exam_date'}

    if not required_names.issubset(tag_names):
        return failed("test18", fields_not_found)

    data = get_course_dict()

    page = url_class.send_form(url, "make_course", data)
    if page.status_code != 200:
        return failed('test18', errors.course_did_not_make)

    return test11_1(url_class, "18", data)
