from bs4 import BeautifulSoup

from errors import profile_link_error, first_name_filed_error, last_name_field_error, user_name_filed_error
from fail_pass import failed, passed


def test8(url_class):
    first_name = "test"
    last_name = "8"
    username = "test8"
    password = "OlDpishExcel18&#"
    data = dict(first_name=first_name, last_name=last_name, username=username, email="test8@gmail.com", password1=password,
                password2=password)

    url_class.reg_and_log(data)

    url = url_class.get_profile_url()
    if not url:
        return failed("test8", profile_link_error)

    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')


    print(soup.prettify()[:5000])
    first_name_tag = soup.find('span', id="text_first_name")
    print(first_name_tag)
    print(first_name)
    if (not first_name_tag) or not first_name_tag.get_text().__contains__(first_name):
        return failed("test8", first_name_filed_error)

    last_name_tag = soup.find('span', id="text_last_name")
    if (not last_name_tag) or not last_name_tag.get_text().__contains__(last_name):
        return failed("test8", last_name_field_error)

    user_name_tag = soup.find('span', id="text_user_name")
    if (not user_name_tag) or not user_name_tag.get_text().__contains__(username):
        return failed("test8", user_name_filed_error)

    return passed("test8")


