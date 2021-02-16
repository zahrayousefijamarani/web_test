from errors import panel_link_error, panel_page_error, panel_link_visible_error
from fail_pass import failed, passed


def test10(url_class):

    url_class.logout()
    url = url_class.get_panel_url()
    if url:
        return failed("test10", panel_link_visible_error)

    data = dict(first_name="test", last_name="10", username="test10", email="test10@gmail.com", password1="OlDpishExcel18&#",
                password2="OlDpishExcel18&#")
    url_class.reg_and_log(data)

    url = url_class.get_panel_url()
    if not url:
        return failed("test10", panel_link_error)

    page = url_class.client.get(url)
    if page.status_code != 200:
        return failed("test10", panel_page_error)

    return passed("test10")

