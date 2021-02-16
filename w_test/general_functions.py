import requests

import string
import random
from random import seed

g_course_number = random.randrange(0, 100)


def get_random_course_number():
    return random.randint(1, 100000000)
    global g_course_number
    g_course_number += 1
    return g_course_number


def get_course_dict(course_number=None, department='comp', name='statics', group_number='1',
                    teacher='be',
                    start_time='15:00', end_time='16:30',
                    first_day='0', second_day='1', exam_date='1398-08-24'):
    if not course_number:
        course_number = get_random_course_number()
    course_data = dict(department=department, name=name, group_number=group_number, course_number=course_number,
                       teacher=teacher, start_time=start_time, end_time=end_time,
                       first_day=first_day, second_day=second_day, exam_date=exam_date)
    return course_data


def get_course_id(course):
    return course['course_number'].__str__() + "_" + course['group_number'].__str__()
