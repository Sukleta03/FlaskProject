import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models import StudentModel, GroupModel, CourseModel, StudentCourse
from config import TestConfig
from app.create_db import init_db


class DataBaseTests(unittest.TestCase):
    def create_models(self):
        group = GroupModel(group_id=1,
                           group_name="PE-21")
        self.session.add(group)
        self.session.commit()
        course = CourseModel(course_id=1,
                             course_name='Math',
                             description='Description will be soon!!!')
        self.session.add(course)
        self.session.commit()
        student = StudentModel(student_id=1,
                               first_name="Dima",
                               last_name="Sukelta",
                               group_name="PE-21")
        student.add_course(course)
        self.session.add(student)
        self.session.commit()

    def setUp(self):
        db_url = TestConfig.SQLALCHEMY_DATABASE_URI
        engine = create_engine(db_url, echo=True)
        init_db(engine)
        self.session = Session(bind=engine)
        self.create_models()

    def test_student(self):
        student = (self.session.query(StudentModel).filter(StudentModel.student_id == 1).first())
        self.assertEqual(student.student_id, 1)
        self.assertEqual(student.first_name, "Dima")
        self.assertEqual(student.last_name, "Sukelta")
        self.assertEqual(student.group_name, "PE-21")

    def test_group(self):
        group = (self.session.query(GroupModel).filter(GroupModel.group_id == 1).first())
        self.assertEqual(group.group_id, 1)
        self.assertEqual(group.group_name, "PE-21")

    def test_course(self):
        course = (self.session.query(CourseModel).filter(CourseModel.course_id == 1).first())
        self.assertEqual(course.course_id, 1)
        self.assertEqual(course.course_name, "Math")
        self.assertEqual(course.description, "Description will be soon!!!")

    def test_student_course(self):
        student_course = (self.session.query(StudentCourse).filter(StudentCourse.student_id == 1).first())
        self.assertEqual(student_course.student_id, 1)
        self.assertEqual(student_course.course_id, 1)

    def test_manu_to_many(self):
        query = self.session.query(StudentModel.first_name, StudentModel.last_name,
                                   StudentModel.group_name, CourseModel.course_name) \
            .join(StudentCourse, StudentModel.student_id == StudentCourse.student_id) \
            .join(CourseModel, StudentCourse.course_id == CourseModel.course_id) \
            .filter(StudentModel.student_id == 1).all()

        self.assertEqual(query[0], ('Dima', 'Sukelta', 'PE-21', 'Math'))

    def tearDown(self):
        self.session.close()
