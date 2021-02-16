import requests
from bs4 import BeautifulSoup
import urllib.parse
from general_functions import get_course_id


# base_url = "http://127.0.0.1:8000"


# base_url = "http://192.168.197.60:8000/"
# base_url = "http://btwitter.pythonanywhere.com/"

def validate_url(url1, url2):
    if url2 == ".":
        return url1
    return urllib.parse.urljoin(url1 + "/", url2)


class URL:
    def __init__(self):
        self.base_url = ''
        self.client = requests.session()

    def get_url(self, id_name):
        url = self.base_url
        page = self.client.get(self.base_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # print("!!!!!!!!!!!!!!", soup.prettify()[:5000])
        tag = soup.find('a', id=id_name)
        if not tag:
            return None
        else:
            return validate_url(url, tag.get('href'))

    def get_home_url(self):
        return self.base_url + "/"

    def get_register_url(self):
        url = self.get_exit_url()
        if url:
            self.client.get(url)
        return self.get_url("register")

    def get_login_url(self):
        self.logout()
        self.logout_from_admin()
        return self.get_url("login")

    def get_profile_url(self):
        return self.get_url("profile")

    def get_panel_url(self):
        return self.get_url("panel")

    def get_exit_url(self):

        return self.get_url("logout")

    def get_contact_us_url(self):
        return self.get_url('contact_us')

    def get_edit_profile_url(self):
        url = self.get_profile_url()
        page = self.client.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        tag = soup.find('a', id='setting')
        if not tag:
            return None
        else:
            return validate_url(self.base_url, tag.get('href'))

    def get_new_course_url(self):
        url = self.get_panel_url()
        page = self.client.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        tag = soup.find('a', id='make_new_course')
        if not tag:
            return None
        else:
            return validate_url(self.base_url, tag.get('href'))

    # safhe namaye vahed
    def get_courses_urls(self):
        url = self.get_panel_url()
        page = self.client.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        link = soup.find('a', id='courses')
        if not link:
            return None
        else:
            return validate_url(self.base_url, link.get('href'))

    def login_as_admin(self):
        self.logout_from_admin()
        self.logout()
        url = self.base_url + "/admin/login/?next=/admin/"
        username = "admin"
        password = "admin123456"
        csrf = self.client.get(url).cookies['csrftoken']

        data = dict(username=username, password=password, csrfmiddlewaretoken=csrf)
        page = self.client.post(url, data=data, headers=dict(Referer=url))
        return page

    def logout_from_admin(self):
        url = self.base_url + "/admin/logout/"
        page = requests.get(url)
        return page

    def reg_and_log(self, data):
        self.logout()
        self.register(self.get_register_url(), data)
        self.logout()
        data = dict(username=data['username'], password=data['password1'])
        return self.login(self.get_login_url(), data)

    def make_course(self, data):
        self.login_as_admin()
        url = self.get_new_course_url()
        page = self.send_form(url, "make_course", data)
        return page

    def add_course(self, soup, course):
        all_div = soup.find('div', id='all_courses')
        course_div = all_div.find(
            lambda tag: tag.name == "div" and tag.get('class')and get_course_id(course) in tag.get('class'))
        add_link = course_div.find_all(lambda tag: tag.name == "a" and tag.get('class')and 'add' in tag.get('class'))

        page = self.client.get(validate_url(self.base_url, add_link[0]['href']))
        return page

    def logout(self):
        self.logout_from_admin()
        url = self.get_exit_url()
        if not url:
            return
        page = self.client.get(url)
        return page

    # def post_a_form(self, url, data):
    #     csrf = self.client.get(url).cookies['csrftoken']
    #
    #     data = dict(**data, **dict(csrfmiddlewaretoken=csrf))
    #     page = self.client.post(url, data=data, headers=dict(Referer=url))
    #     return page

    def register(self, url, data):
        return self.send_form(url, "register_form", data)

    # data is a dict containing 'username', 'password'
    def login(self, url, data):
        return self.send_form(url, "login_form", data)

    def get_form_method(self, url, id_):
        page = self.client.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        form_div = soup.find("form", id=id_)
        if not form_div:
            return None, None
        method = form_div.get('method')
        action = form_div.get('action')
        new_url = url
        if action:
            new_url = validate_url(new_url, action)

        return new_url, method

    def send_form(self, url, id_, data):
        # print(url, id_, data)
        csrf_url = url
        url, method = self.get_form_method(url, id_)
        # print(url, method)
        if not url:
            return None
        if method.lower() == "post":
            csrf = self.client.get(csrf_url).cookies['csrftoken']
            data = dict(**data, **dict(csrfmiddlewaretoken=csrf))
            page = self.client.post(url, data=data, headers=dict(Referer=url))
        else:
            page = self.client.get(url, params=data)
        soup = BeautifulSoup(page.content, 'html.parser')

        # print(soup.prettify()[:5000])
        # print("~~~~~", id_)

        return page

