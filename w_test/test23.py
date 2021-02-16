import random
import string

from bs4 import BeautifulSoup

from errors import markdown_checkbox_not_found, markdown_comment_error, fail_to_comment
from fail_pass import failed, passed
from general_functions import get_course_dict, get_course_id
from urls import validate_url


def random_generator(size=6, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for x in range(size))


def get_markdown():
    # markdown = "## {} \n **{}** `{}` \n| {} | {} |\n|---|---|\n" \
    #            "| {} | {} |"
    #
    # text = "<h2>{}</h2><p><strong>{}</strong><code>{}</code></p><table><thead><tr><th>{}</th><th>{}</th></tr></thead>" \
    #        "<tbody><tr><td>{}</td><td>{}</td></tr></tbody></table>"
    markdown = "**{}** `{}`"

    text = "<strong>{}</strong><code>{}</code>"
    l = []
    for i in range(7):
        l.append(random_generator())
    return markdown.format(*l), text.format(*l)


def test23(url_class):
    first_name = "test"
    last_name = "23"
    username = "test23"
    password = "OlDpishExcel18"
    data = dict(first_name=first_name, last_name=last_name, username=username, email="test23@gmail.com",
                password1=password,
                password2=password)

    url_class.reg_and_log(data)

    course_page_url = url_class.get_courses_urls()
    client = url_class.client
    course_data = get_course_dict()

    url_class.make_course(course_data)

    page = client.get(course_page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_div = soup.find('div', id='all_courses')
    course_div = all_div.find(lambda tag: tag.name == "div" and tag.get('class')and get_course_id(course_data) in tag.get('class'))
    details_link = course_div.find(lambda tag: tag.name == "a" and tag.get('class')and "details" in tag.get('class'))

    course_page_url = validate_url(url_class.base_url, details_link['href'])

    page = client.get(course_page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    comments_div = soup.find('div', id='comments')
    checkbox = comments_div.find('input', id="markdown_comment")
    if not checkbox:
        return failed("test23", markdown_checkbox_not_found)

    markdown, html_text = get_markdown()
    data = dict(comment=markdown, markdown_comment=True)
    page = url_class.send_form(course_page_url, "comment_form", data)
    if page.status_code != 200:
        return failed('test22', fail_to_comment)

    page = url_class.client.get(course_page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    comment_div = soup.find('div', id='comments')
    comment_div_divs = comment_div.find_all('div')
    for div in comment_div_divs:
        text = div.find(lambda tag: tag.name == "p" and tag.get('class')and "text" in tag.get('class'))
        if text:
            text = ''.join(str(text).split())
            if text.__contains__(html_text):
                return passed('test23')

    return failed("test23", markdown_comment_error)

