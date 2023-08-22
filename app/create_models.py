from app.models import StudentModel, CourseModel, GroupModel
from app.data import course_func, group_func, student_generator, random_courses
from . import db


def fill_data():
    group_list = group_func(10)
    course_objects_list = []
    course_list = course_func()
    with db.session() as session:
        for i, course in enumerate(course_list):
            new_course = CourseModel(course_id=i+1,
                                     course_name=course,
                                     description="Description will be soon!!!")
            course_objects_list.append(new_course)
            session.add(new_course)
        session.commit()
        for id, group in enumerate(group_list):
            new_group = GroupModel(group_id=id + 1,
                                   group_name=group)
            session.add(new_group)
        session.commit()
        for id, student, group in student_generator(group_list, 200):
            student_split = student.split()
            new_student = StudentModel(student_id=id + 1,
                                       group_name=group,
                                       first_name=student_split[0],
                                       last_name=student_split[1])
            courses = random_courses()
            for id in courses:
                new_student.add_course(course_objects_list[id])
            session.add(new_student)
        session.commit()
    session.close()


