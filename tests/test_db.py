import unittest
from flask import Flask
from app.models import StudentModel, GroupModel, CourseModel, StudentCourse
from config import TestConfig
from app import db


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
            student = (db.session.query(StudentModel).filter(StudentModel.student_id == 1).first())
        self.assertEqual(student.student_id, 1)
        self.assertEqual(student.first_name, "Dima")
        self.assertEqual(student.last_name, "Sukelta")
        self.assertEqual(student.group_name, "PE-21")

    def test_group(self):
        with self.app.app_context():
            group = (db.session.query(GroupModel).filter(GroupModel.group_id == 1).first())
        self.assertEqual(group.group_id, 1)
        self.assertEqual(group.group_name, "PE-21")

    def test_course(self):
        with self.app.app_context():
            course = (db.session.query(CourseModel).filter(CourseModel.course_id == 1).first())

        self.assertEqual(course.course_id, 1)
        self.assertEqual(course.course_name, "Math")
        self.assertEqual(course.description, "Description will be soon!!!")

    def test_student_course(self):
        with self.app.app_context():
            student_course = (db.session.query(StudentCourse).filter(StudentCourse.student_id == 1).first())
        self.assertEqual(student_course.student_id, 1)
        self.assertEqual(student_course.course_id, 1)

    def test_manu_to_many(self):
        with self.app.app_context():
            query = db.session.query(StudentModel.first_name, StudentModel.last_name,
                                   StudentModel.group_name, CourseModel.course_name) \
            .join(StudentCourse, StudentModel.student_id == StudentCourse.student_id) \
            .join(CourseModel, StudentCourse.course_id == CourseModel.course_id) \
            .filter(StudentModel.student_id == 1).all()

        self.assertEqual(query[0], ('Dima', 'Sukelta', 'PE-21', 'Math'))


