import random
from faker import Faker

faker = Faker()


def student_func(a):
    first_name_list = [faker.first_name() for x in range(20)]
    last_name_list = [faker.first_name() for x in range(20)]
    student_list = []
    for i in range(a):
        name_line = first_name_list[random.randint(0, 19)] + " " + last_name_list[random.randint(0, 19)]
        student_list.append(name_line)
    return student_list


def course_func():
    return ["math", "Art",
           "English", "Music",
           "History", "Geography",
           "Swimming", "Science",
           "Biology", "Information technolohy"]


def group_name():
    random_letter_1 = str(chr(random.randint(ord('A'), ord('Z'))))
    random_letter_2 = chr(random.randint(ord('A'), ord('Z')))
    random_num_1 = str(random.randint(1, 9))
    random_num_2 = str(random.randint(1, 9))
    return random_letter_1+random_letter_2+"-"+random_num_1+random_num_2


def group_func(num):
    group_list = [group_name() for x in range(num)]
    return group_list


def student_generator(group_list, num):
    first_num = 0
    last_num = random.randint(10, 29)
    group = 0
    i = 0
    student_list = student_func(num)
    while last_num <= num and group < 10:
        for student in student_list[first_num:last_num]:
            yield i, student, group_list[group]
            i += 1
        first_num = last_num
        last_num += random.randint(9, 29)
        group += 1
    if first_num < num:
        for student in student_list[first_num:]:
            group = None
            yield i, student, group
            i += 1


def random_courses():
    num_list = [random.randint(0, 9) for i in range(random.randint(1, 3))]
    return num_list