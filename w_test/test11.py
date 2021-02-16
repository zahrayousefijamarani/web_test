from bs4 import BeautifulSoup

import errors
from errors import form_div_error, fields_not_found, make_new_course_link_error
from fail_pass import failed
from general_functions import  get_course_dict
from test11_2 import test11_1


def test11(url_class):

    first_name = "test"
    last_name = "11"
    username = "test11"
    password = "OlDpishExcel18&#"
    data = dict(first_name=first_name, last_name=last_name, username=username, email="test11@gmail.com", password1=password,
                password2=password)

    url_class.reg_and_log(data)
    url = url_class.get_new_course_url()
    # url = base_url + '/course/add'
    if not url:
        url_class.logout()
        url_class.login_as_admin()
        url = url_class.get_new_course_url()
        if not url:
            return failed("test11", make_new_course_link_error)

    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    form = soup.find('form', id="make_course")
    if not form:
        return failed("test11", form_div_error)

    inputs = form.find_all('input') + form.find_all('select')
    tag_names = set([tag.get('name') for tag in inputs])

    required_names = {'department', 'name', 'group_number', 'course_number', 'teacher', 'start_time', 'end_time',
                      'first_day', 'second_day'}

    if not required_names.issubset(tag_names):
        return failed("test11", fields_not_found)

    data = get_course_dict()

    page = url_class.send_form(url, "make_course", data)
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())
    if page.status_code != 200:
        return failed('test11', errors.course_did_not_make)

    return test11_1(url_class, "11", data)
