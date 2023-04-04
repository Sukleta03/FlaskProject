import unittest
from flask import Flask
from app.models import StudentModel, GroupModel, CourseModel, StudentCourse
from config import TestConfig
from app import db
from app.orm_querys import get_student, update_student, \
    delete_student_by_id, get_students, add_student_to_table, \
    get_group, update_group, delete_group_by_id, get_groups, add_group_to_table, \
    get_course_by_id, update_course, delete_course, get_courses, students_from_course,\
    add_course_to_table, add_student_to_course, get_groups_with_less_students_count, \
    delete_student_from_course


def create_models():
    with db.session() as session:
        group = GroupModel(group_id=1,
                           group_name="PE-21")
        session.add(group)
        session.commit()
        course = CourseModel(course_id=1,
                             course_name='Math',
                             description='Description will be soon!!!')
        session.add(course)
        session.commit()
        student = StudentModel(student_id=1,
                               first_name="Dima",
                               last_name="Sukelta",
                               group_name="PE-21")
        student.add_course(course)
        session.add(student)
        session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object(TestConfig)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        create_models()
    return app


class DataBaseTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()

    def test_student(self):
        with self.app.app_context():
            data = get_student(1)
        self.assertEqual(data, (1, 'Dima', 'Sukelta', 'PE-21'))

    def test_update_student(self):
        with self.app.app_context():
            data = update_student(1, 'Dima', 'Sukelta', 'PE-21')
        self.assertEqual(data, (1, 'Dima', 'Sukelta', 'PE-21'))

    def test_get_studets(self):
        with self.app.app_context():
            data = get_students()
        self.assertEqual(data, [{'first_name': 'Dima', 'group_name': 'PE-21',
                                 'last_name': 'Sukelta', 'student_id': 1}])

    def test_add_student_to_table(self):
        with self.app.app_context():
            data = add_student_to_table(2, 'Ivan', 'Ivanov', 'PE-21')
        self.assertEqual(data, (2, 'Ivan', 'Ivanov', 'PE-21'))

    def test_get_group(self):
        with self.app.app_context():
            data = get_group(1)
        self.assertEqual(data, (1, 'PE-21'))

    def test_update_group(self):
        with self.app.app_context():
            data = update_group(1, 'PE-21')
        self.assertEqual(data, (1, 'PE-21'))

    def test_delete_group_by_id(self):
        with self.app.app_context():
            data = delete_group_by_id(1)
        self.assertEqual(data, (1, 'PE-21'))

    def test_get_groups(self):
        with self.app.app_context():
            data = get_groups()
        self.assertEqual(data, [{'group_id': 1, 'group_name': 'PE-21'}])

    def test_add_group_to_table(self):
        with self.app.app_context():
            data = add_group_to_table(2, 'RA-22')
        self.assertEqual(data, (2, 'RA-22'))

    def test_get_course_by_id(self):
        with self.app.app_context():
            data = get_course_by_id(1)
        self.assertEqual(data, (1, 'Math', 'Description will be soon!!!'))

    def test_delete_course(self):
        with self.app.app_context():
            data = delete_course(1)
        self.assertEqual(data, (1, 'Math'))

    def test_update_course(self):
        with self.app.app_context():
            data = update_course(1, 'Math')
        self.assertEqual(data, (1, 'Math'))

    def test_get_courses(self):
        with self.app.app_context():
            data = get_courses()
        self.assertEqual(data, [{'course_id': 1, 'course_name': 'Math', 'description': 'Description will be soon!!!'}])

    def test_add_course_to_table(self):
        with self.app.app_context():
            data = add_course_to_table(2, 'Python', 'Description will be soon!!!')
        self.assertEqual(data, (2, 'Python'))

    def test_get_groups_with_less_students_count(self):
        with self.app.app_context():
            data = get_groups_with_less_students_count(5)
        self.assertEqual(data, [{'group_name': 'PE-21', 'student_count': 1}])

    def test_students_from_course(self):
        with self.app.app_context():
            data = students_from_course(1)
        self.assertEqual(data, [('Dima', 'Sukelta', 'Math')])

    def test_delete_student_from_course(self):
        with self.app.app_context():
            data = delete_student_from_course(1, 1)
        self.assertEqual(data, (1, 1))

    def test_add_student_to_course(self):
        with self.app.app_context():
            new_course = CourseModel(course_id=3, course_name='Java', description='Description will be soon!!!')
            db.session.add(new_course)
            db.session.commit()
            data = add_student_to_course(1, ['Java'])
        self.assertEqual(data, (1, ['Java']))

    def test_delete_student_by_id(self):
        with self.app.app_context():
            data = delete_student_by_id(1)
        self.assertEqual(data, 1)