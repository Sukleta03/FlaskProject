from sqlalchemy.orm import sessionmaker, declarative_base, relationship, backref
from sqlalchemy import Column, String, Integer, ForeignKey
import uuid



Base = declarative_base()
Session = sessionmaker()


class StudentCourse(Base):
    # many-to-many relationship
    __tablename__ = 'student_course'

    id = Column(String, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'), primary_key=True)

    student = relationship("StudentModel", backref=backref("student_course", cascade="all, delete-orphan"))
    course = relationship("CourseModel", backref=backref("student_course", cascade="all, delete-orphan"))

    def __init__(self, student=None, course=None):
        self.id = uuid.uuid4().hex
        self.student = student
        self.course = course


class GroupModel(Base):
    __tablename__ = 'groups'

    group_id = Column(Integer(), primary_key=True)
    group_name = Column(String(), unique=True)

    def __repr__(self) -> str:
        return f"group_id={self.group_id!r}"\
                f"group_name={self.group_name!r}"


class StudentModel(Base):
    __tablename__ = 'students'

    student_id = Column(Integer(),  primary_key=True)
    group_name = Column(String(), ForeignKey('groups.group_name'))
    first_name = Column(String())
    last_name = Column(String())

    def add_course(self, course):
        self.student_course.append(StudentCourse(course=course))

    def __repr__(self) -> str:
        return f"first_name={self.first_name!r}," \
               f" last_name={self.last_name!r}," \
               f" group_name={self.group_name!r},"



class CourseModel(Base):
    __tablename__ = 'courses'

    course_id = Column(Integer(), primary_key=True)
    course_name = Column(String(), unique=True)
    description = Column(String())

    def __repr__(self) -> str:
        return f"course name={self.course_name!r},"\
               f"description={self.description!r}"