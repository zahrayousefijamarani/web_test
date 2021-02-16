from bs4 import BeautifulSoup

import errors
from fail_pass import failed, passed
from general_functions import get_course_dict, get_course_id


def test14(url_class):
    password = "OlDpishExcel18&#"
    data = dict(first_name="test", last_name="15", username="test14", email="test14@gmail.com", password1=password,
                password2=password)
    url_class.reg_and_log(data)

    url = url_class.get_courses_urls()
    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    search_div = soup.find('form', id='search_form')
    if not search_div:
        return failed('test14', errors.search_form_error)
    buttons = search_div.find_all("button", attrs={'name': "submit"})
    if not buttons:
        return failed("test14", errors.submit_button_not_found)

    check_boxes = soup.find_all('input')
    tag_names = set([tag.get('name') for tag in check_boxes])

    required_names = {'search_query', 'department', 'teacher', 'course'}

    if not required_names.issubset(tag_names):
        return failed('test14', errors.have_not_all_inputs)

    courses_data = [get_course_dict(department="ce", name="ap", teacher="saba"),
                    get_course_dict(department="ce", name="saba", teacher="saba"),
                    get_course_dict(department="math", name="math1", teacher="other"),
                    get_course_dict(department="math", name="math2", teacher="other"),
                    get_course_dict(department="math", name="saba", teacher="other"),
                    get_course_dict(department="math", name="saba", teacher="other")]

    for i in courses_data:
        url_class.make_course(i)

    data1 = dict(search_query='saba', department=False, teacher=True, course=True)

    page = url_class.send_form(url, "search_form", data1)
    if page.status_code != 200:
        return failed("test14", errors.can_not_search)

    soup = BeautifulSoup(page.content, 'html.parser')

    search_result_div = soup.find("div", id="search_result")
    if not search_result_div:
        return failed("test14", errors.search_result_div_error)

    divs = search_result_div.find_all("div")

    check_find = True
    duplicate = False
    for course in courses_data[:2] + courses_data[4:]:
        check = False
        t = 0
        # print(course)
        for res_div in divs:
            if res_div.get("class") and get_course_id(course) in res_div.get("class"):
                all_fields_ok = True
                all_fields_ok = all_fields_ok and res_div.getText().__contains__(course['name'])
                all_fields_ok = all_fields_ok and res_div.getText().__contains__(course['teacher'])
                check = check or all_fields_ok
                t += 1
                # print(res_div)
        if t > 1:
            duplicate = True
        check_find = check_find and check

    if not check_find:
        return failed("test14", errors.result_not_found)

    if duplicate:
        return failed("test14", errors.duplicate_search)

    check_not_find = True
    for course in courses_data[2:4]:
        for res_div in divs:
            if res_div.get("class") and get_course_id(course) in res_div.get("class"):
                check_not_find = False

    if not check_not_find:
        return failed("test14", errors.more_result_found)

    return passed("test14")
