from bs4 import BeautifulSoup

from errors import register_with_existing_username, error_div_error, register_with_wrong_passes
from fail_pass import failed, passed


def check_user_not_exist(url_class, url):
    data = dict(first_name="saba", last_name="h", username="test4", email="saba@gmail.com", password1="OlDpishExcel18&#",
                password2="OlDpishExcel18&#")

    url_class.register(url, data)
    page = url_class.register(url, data)
    soup = BeautifulSoup(page.content, 'html.parser')
    error = soup.find('div', id="errors")
    if not error:
        return failed("test4", error_div_error)
    error_text = error.getText()
    if not error_text.__contains__('نام کاربری شما در سیستم موجود است'):
        return failed("test4", register_with_existing_username)
    return None


def check_pass1_and_pass2_match(url_class, url):
    data = dict(first_name="saba2", last_name="h2", username="test4_2", email="test4@gmail.com",
                password1="OlDpishExcel18&#",
                password2="saba1234567911123")

    page = url_class.register(url, data)
    soup = BeautifulSoup(page.content, 'html.parser')
    error = soup.find('div', id="errors")
    if not error:
        return failed("test4", error_div_error)
    error_text = error.getText()
    if not error_text.__contains__('گذرواژه و تکرار گذرواژه یکسان نیستند'):
        return failed("test4", register_with_wrong_passes)
    return None


def test4(url_class):
    url = url_class.get_register_url()

    first_test = check_user_not_exist(url_class, url)
    if first_test:
        return first_test

    second_test = check_pass1_and_pass2_match(url_class, url)
    if second_test:
        return second_test

    return passed("test4")
