from bs4 import BeautifulSoup

from errors import search_form_error, fields_not_found, submit_button_not_found, can_not_search, \
    search_result_div_error, result_not_found, more_result_found
from fail_pass import failed, passed
from general_functions import  get_course_dict, get_course_id


def test13(url_class):

    password = "OlDpishExcel18&#"
    courses_data = dict(first_name="test", last_name="14", username="test13", email="test13@gmail.com",
                        password1=password,
                        password2=password)
    url_class.reg_and_log(courses_data)

    url = url_class.get_courses_urls()
    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    div = soup.find("form", id="search_form")
    if not div:
        return failed("test13", search_form_error)
    inputs = div.find_all("input", attrs={'name': "search_query"})
    if not inputs:
        return failed("test13", fields_not_found)
    buttons = div.find_all("button",  attrs={'name': "submit"})
    if not buttons:
        return failed("test13", submit_button_not_found)

    courses_data = list()
    courses_data.append(get_course_dict(department="comp", name="ds"))
    courses_data.append(get_course_dict(department="comp", name="ap"))
    courses_data.append(get_course_dict(department="math", name="math1"))
    courses_data.append(get_course_dict(department="math", name="math2"))

    for d in courses_data:
        url_class. make_course(d)

    search_data = dict(search_query="comp", department=True)
    page = url_class.send_form(url, "search_form", search_data)

    if page.status_code != 200:
        return failed("test13", can_not_search)

    soup = BeautifulSoup(page.content, 'html.parser')
    search_result_div = soup.find("div", id="search_result")

    if not search_result_div:
        return failed("test13", search_result_div_error)

    divs = search_result_div.find_all("div")

    check_find = True
    for course in courses_data[0:2]:
        check = False
        for res_div in divs:
            if res_div.get("class") and get_course_id(course) in res_div.get("class"):
                all_fields_ok = True
                all_fields_ok = all_fields_ok and res_div.getText().__contains__(course['name'])
                all_fields_ok = all_fields_ok and res_div.getText().__contains__(course['teacher'])
                check = check or all_fields_ok
        check_find = check_find and check

    if not check_find:
        return failed("test13", result_not_found)

    check_not_find = True
    for course in courses_data[2:]:
        for res_div in divs:
            check_not_find = check_not_find and (not res_div.get("class") or not get_course_id(course) in res_div.get("class"))

    if not check_not_find:
        return failed("test13", more_result_found)

    return passed("test13")
