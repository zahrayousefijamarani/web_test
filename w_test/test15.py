import requests
from bs4 import BeautifulSoup

import urls
from errors import file_input_field_error, img_tag_error, profile_image_error, img_src_error

from fail_pass import failed, passed
import shutil

BASE_DIR = "/home/ubuntu/contest/w_test/"


def test15(url_class):
    password = "OlDpishExcel18&#"
    data = dict(first_name="test", last_name="16", username="test15", email="test15@gmail.com", password1=password,
                password2=password)
    url_class.reg_and_log(data)

    url = url_class.get_edit_profile_url()

    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    upload_file = soup.find_all('input', type="file")
    if not upload_file:
        return failed("test15", file_input_field_error)

    files = {'profile_image': open(BASE_DIR + "profile_image.jpg", "rb")}
    csrf = url_class.client.get(url).cookies['csrftoken']
    data = dict(csrfmiddlewaretoken=csrf)
    url_class.client.post(url, data=data, files=files)

    url = url_class.get_profile_url()
    page = url_class.client.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    image_tag = soup.find('img', id="profile_image")
    if not image_tag:
        return failed("test15", img_tag_error)

    image_src = image_tag.get("src")
    if not image_src:
        return failed("test15", img_src_error)

    response = requests.get(urls.validate_url(url_class.base_url, image_src), stream=True)
    with open(BASE_DIR + 'profile_image2.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    if open(BASE_DIR + "profile_image.jpg", "rb").read() != open(BASE_DIR + "profile_image2.jpg", "rb").read():
        return failed("test15", profile_image_error)

    return passed("test15")
