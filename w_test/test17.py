from bs4 import BeautifulSoup

from errors import my_courses_div_error, remove_link_not_found, can_not_remove, course_not_found_in_my_courses, \
    removed_course_still_in_my_course, removed_course_not_in_all_course
from fail_pass import failed, passed
from general_functions import get_course_dict, get_course_id
from urls import validate_url


def test17(url_class):
    first_name = "test"
    last_name = "18"
    username = "test17"
    password = "OlDpishExcel18"
    data = dict(first_name=first_name, last_name=last_name, username=username, email="test17@gmail.com", password1=password,
                password2=password)

    url_class.reg_and_log(data)

    url = url_class.get_courses_urls()

    courses_data = []
    for i in range(1, 10):
        course = get_course_dict()
        courses_data.append(course)
        url_class.make_course(course)

    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup)

    for course in courses_data:
        url_class.add_course(soup, course)

    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    my_div = soup.find('div', id='my_courses')
    if not my_div:
        return failed('test17', my_courses_div_error)

    courses_div = my_div.find_all('div')
    course = courses_data[0]

    found_course = False
    for div in courses_div:
        if div.get("class") and get_course_id(course) in div.get("class"):
            found_course = True
            remove_link = div.find(lambda tag: tag.name == "a" and tag.get('class')and 'remove' in tag.get('class'))
            if not remove_link:
                return failed("test17", remove_link_not_found)
            page = url_class.client.get(validate_url(url_class.base_url, remove_link['href']))
            if page.status_code != 200:
                return failed("test17", can_not_remove)

    if not found_course:
        return failed("test17", course_not_found_in_my_courses)

    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    my_div = soup.find('div', id='my_courses')
    courses_div = my_div.find_all('div')

    for div in courses_div:
        if div.get("class") and get_course_id(course) in div.get("class"):
            return failed("test17", removed_course_still_in_my_course)

    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_div = soup.find('div', id='all_courses')
    all_courses_div = all_div.find_all('div')

    found_course = False
    for div in all_courses_div:
        if div.get("class") and get_course_id(course) in div.get("class"):
            found_course = True

    if not found_course:
        return failed("test17", removed_course_not_in_all_course)

    return passed("test17")

