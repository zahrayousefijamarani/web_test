from bs4 import BeautifulSoup

from errors import edit_profile_link_error, form_div_error, fields_not_found, first_name_change_error, \
    last_name_change_error
from fail_pass import failed, passed


def test9(url_class):

    first_name = "test"
    last_name = "9"
    username = "test9"
    password = "OlDpishExcel18&#"
    data = dict(first_name=first_name, last_name=last_name, username=username, email="test9@gmail.com",
                password1=password, password2=password)

    url_class.reg_and_log(data)

    url = url_class.get_edit_profile_url()
    if not url:
        return failed("test9", edit_profile_link_error)

    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    form = soup.find('form', id="setting_form")
    if not form:
        return failed("test9", form_div_error)

    inputs = form.find_all('input')
    tag_names = set([tag.get('name') for tag in inputs])

    required_names = {'first_name', 'last_name'}

    if not required_names.issubset(tag_names):
        return failed("test9", fields_not_found)

    client = url_class.client
    second_name = 'av'
    second_last_name = 'awq'
    data1 = dict(first_name=first_name, last_name=last_name)
    data2 = dict(first_name=second_name, last_name=second_last_name)

    page = url_class.send_form(url, "setting_form", data1)

    page = client.get(url_class.get_profile_url())
    soup = BeautifulSoup(page.content, 'html.parser')

    first_name_tag = soup.find('span', id="text_first_name")
    if (not first_name_tag) or not first_name_tag.get_text().__contains__(first_name):
        return failed("test9", first_name_change_error)

    last_name_tag = soup.find('span', id="text_last_name")
    if (not last_name_tag) or not last_name_tag.get_text().__contains__(last_name):
        return failed("test9", last_name_change_error)

    page = url_class.send_form(url, "setting_form", data2)
    page = client.get(url_class.get_profile_url())
    soup = BeautifulSoup(page.content, 'html.parser')

    first_name_tag = soup.find('span', id="text_first_name")
    if (not first_name_tag) or not first_name_tag.get_text().__contains__(second_name):
        return failed("test9", first_name_change_error)

    last_name_tag = soup.find('span', id="text_last_name")
    if (not last_name_tag) or not last_name_tag.get_text().__contains__(second_last_name):
        return failed("test9", last_name_change_error)

    return passed("test9")


