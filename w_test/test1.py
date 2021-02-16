import urllib.request
from bs4 import BeautifulSoup

from errors import navbar_error, login_link_error, register_link_error, homepage_link_error, homepage_href_error, \
    welcome_error
from fail_pass import failed, passed


def test1(url_class):
    base_url = url_class.base_url
    request = urllib.request.Request(base_url)
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html, 'html.parser')
    navbar = soup.find("div", id='navbar')
    if not navbar:
        return failed("test1", navbar_error)

    login = navbar.find('a', id='login')
    if not login:
        return failed("test1", login_link_error)

    register = navbar.find('a', id='register')
    if not register:
        return failed("test1", register_link_error)

    home = navbar.find('a', id='homepage')
    if not home:
        return failed("test1", homepage_link_error)
    if home['href'] != '/':
        return failed("test1", homepage_href_error)

    if not soup.getText().__contains__("سلام. به سامانه‌ی انتخاب واحد مجازی خوش آمدید."):
        return failed("test1", welcome_error)
    return passed("test1")
