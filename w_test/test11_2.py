from bs4 import BeautifulSoup

import errors
from fail_pass import failed, passed


# edame test 11
from general_functions import get_course_id, get_course_dict


def test11_1(url_class, test_number="11", class_data=get_course_dict(11111)):
    url = url_class.get_courses_urls()
    if not url:
        return failed("test11", errors.courses_link_error)

    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_div = soup.find('div', id='all_courses')
    if not all_div:
        return failed('test11', errors.all_course_div_error)

    course_div = all_div.find(lambda tag: tag.name == "div" and tag.get('class')and get_course_id(class_data) in
                                          tag.get('class'))
    if not course_div:
        return failed('test11', errors.course_box_error)

    course_name = course_div.find('h4')
    if not course_name and str(course_name.getText().strip()).__contains__(class_data['name']):
        return failed('test11', errors.course_name_error)

    tags = course_div.find_all('div')
    check = False
    for tag in tags:
        if str(tag.getText().strip()).__contains__(class_data['teacher']):
            check = True
    if not check:
        return failed('test11', errors.lecturer_error)

    check = False
    for tag in tags:
        if str(tag.getText().strip()).__contains__(class_data['department']):
            check = True
    if not check:
        return failed('test11', errors.department_name_error)

    check = False
    for tag in tags:
        if not (str(tag.getText().strip()).__contains__(class_data['start_time']) and
                str(tag.getText().strip()).__contains__(class_data['end_time'])):
            check = True
    if not check:
        return failed('test11', errors.time_error)

    return passed("test" + test_number)
