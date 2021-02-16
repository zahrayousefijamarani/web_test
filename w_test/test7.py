import errors
from fail_pass import failed, passed
from bs4 import BeautifulSoup


def test7(url_class):
    data = dict(first_name="saba", last_name="h", username="test7", email="test7@gmail.com", password1="OlDpishExcel18&#",
                password2="OlDpishExcel18&#")

    url_class.reg_and_log(data)

    url = url_class.get_exit_url()
    if not url:
        return failed("test7", errors.logout_link_error)

    page = url_class.client.get(url)
    if page.url != url_class.get_home_url() and page.url != url_class.get_home_url() + "/":
        return failed('test7', errors.logout_failed)

    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())
    url = url_class.get_login_url()
    if not url:
        return failed('test7', errors.logout_failed)

    url = url_class.get_exit_url()

    # print(url)
    if url:
        return failed('test7', errors.logout_failed)

    return passed('test7')


