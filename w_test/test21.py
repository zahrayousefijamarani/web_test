from bs4 import BeautifulSoup

from errors import fields_not_found, details_link_not_found, course_div_error
from fail_pass import failed, passed
from general_functions import get_course_dict, get_course_id
from urls import validate_url


def get_details_link(url_class,div, course):
    courses_div = div.find_all('div')
    if courses_div:
        for div in courses_div:
            if div.get("class") and get_course_id(course) in div.get("class"):
                details_link = div.find(lambda tag: tag.name == "a" and tag.get('class')and 'details' in tag.get('class'))
                if not details_link:
                    return False, failed("test21", details_link_not_found)
                return True, validate_url(url_class.base_url, details_link['href'])

    return False, failed("test21", course_div_error)


def check_details_page(url_class,url, requirements):
    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tags = soup.find_all("p")
    for req in requirements:
        found = False
        for tag in tags:
            if tag.getText().__contains__(req.__str__()):
                found = True
        if not found:
            return False, failed("test21", fields_not_found)
    return True, None


def check(url_class, url, course, requirements, id_):
    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_div = soup.find('div', id=id_)

    success, obj = get_details_link(url_class,all_div, course)
    if not success:
        return False, obj
    success, obj = check_details_page(url_class,obj, requirements)
    if not success:
        return False, obj
    return True, None


def test21(url_class):
    url_class.login_as_admin()

    url = url_class.get_courses_urls()

    courses_data = get_course_dict()
    requirements = [courses_data['department'], courses_data['group_number'], courses_data['name'],
                    courses_data['course_number'], courses_data['teacher'], courses_data['start_time'],
                    courses_data['end_time']]

    course = courses_data
    url_class.make_course(course)

    success, obj = check(url_class, url, course, requirements, "all_courses")
    if not success:
        return obj

    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    url_class.add_course(soup, course)

    success, obj = check(url_class, url, course, requirements, "my_courses")
    if not success:
        return obj

    return passed("test21")
