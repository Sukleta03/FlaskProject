from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, create_engine, and_
from app.models import GroupModel, StudentModel, CourseModel, StudentCourse
from config import MainConfig


db_url = MainConfig.SQLALCHEMY_DATABASE_URI
engine = create_engine(db_url, echo=True)
session = sessionmaker(bind=engine)()


def get_groups_with_less_students_count(max_students):
    result = (
        session.query(
            GroupModel.group_name,
            func.count(StudentModel.group_name)
        )
        .outerjoin(StudentModel, GroupModel.group_name == StudentModel.group_name)
        .group_by(GroupModel.group_name)
        .having(func.count(StudentModel.group_name) <= max_students)
        .order_by(func.count(StudentModel.group_name).asc())
        .all()
    )
    return result


def students_from_course_by_name(course_name):
    result = (
        session.query(
            StudentModel.first_name,
            StudentModel.last_name,
            CourseModel.course_name
        )
        .select_from(StudentCourse)
        .join(CourseModel, CourseModel.course_id == StudentCourse.course_id)
        .join(StudentModel, StudentModel.student_id == StudentCourse.student_id)
        .filter(CourseModel.course_name == course_name)
        .all()
    )
    return result


def add_student_to_table(student_id, first_name, last_name, group_name):
    new_student = StudentModel(student_id=student_id,
                               first_name=first_name,
                               last_name=last_name,
                               group_name=group_name)
    session.add(new_student)
    session.commit()


def delete_student_by_id(student_id):
    session.query(StudentCourse).filter(StudentCourse.student_id == student_id).delete()
    session.query(StudentModel).filter(StudentModel.student_id == student_id).delete()
    session.commit()


def add_student_to_course(student_id, course_name_list):
    student = session.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    for course_name in course_name_list:
        course = session.query(CourseModel).filter(CourseModel.course_name == course_name).first()

        student.add_course(course)
    session.commit()


def delete_student_from_course(session, student_id, course_name):
    subquery = (
        session.query(StudentModel.student_id)
        .join(StudentCourse, StudentModel.student_id == StudentCourse.student_id)
        .join(CourseModel, StudentCourse.course_id == CourseModel.course_id)
        .filter(StudentModel.student_id == student_id, CourseModel.course_name == course_name)
        .subquery()
    )

    session.query(StudentCourse).filter(
        and_(
            StudentCourse.student_id.in_(subquery.as_scalar()),
            StudentCourse.course_id == (
                session.query(CourseModel.course_id)
                .filter(CourseModel.course_name == course_name)
                .scalar_subquery()
            )
        )
    ).delete(synchronize_session=False)

    session.commit()
