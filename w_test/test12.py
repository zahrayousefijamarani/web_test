from errors import new_course_non_admin_error, new_course_admin_error
from fail_pass import failed, passed


def test12(url_class):

    url_class.logout_from_admin()

    data = dict(first_name="test", last_name="12", username="test12", email="test12@gmail.com", password1="OlDpishExcel18&#",
                password2="OlDpishExcel18&#")
    url_class.reg_and_log(data)

    if url_class.get_new_course_url():
        return failed("test12", new_course_non_admin_error)

    url_class.logout()
    url_class.login_as_admin()
    if not url_class.get_new_course_url():
        return failed("test12", new_course_admin_error)

    return passed("test12")
