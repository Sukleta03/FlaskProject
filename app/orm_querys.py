from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, create_engine, and_
from app.models import GroupModel, StudentModel, CourseModel, StudentCourse
from config import MainConfig


db_url = MainConfig.SQLALCHEMY_DATABASE_URI
engine = create_engine(db_url, echo=True)
session = sessionmaker(bind=engine)()


def get_student(student_id):
    result = session.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    return result


def update_student(student_id, first_name, last_name, group_name):
    student = session.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    student.first_name = first_name
    student.last_name = last_name
    student.group_name = group_name
    session.commit()
    return student_id, first_name, last_name, group_name


def get_students():
    students = session.query(StudentModel).all()
    result = [{'student_id': student.student_id, 'first_name': student.first_name, 'last_name': student.last_name,
             'group_name': student.group_name} for student in students]
    return result


def add_student_to_table(student_id, first_name, last_name, group_name):
    new_student = StudentModel(student_id=student_id,
                               first_name=first_name,
                               last_name=last_name,
                               group_name=group_name)
    session.add(new_student)
    session.commit()
    return student_id, first_name, last_name, group_name


def get_group(group_id):
    result = session.query(GroupModel).filter(GroupModel.group_id == group_id).first()
    return result


def update_group(group_id, group_name):
    group = session.query(GroupModel).filter(GroupModel.group_id == group_id).first()
    group.group_name = group_name
    session.commit()
    return group_id, group_name


def delete_group_by_id(group_id):
    group_name = session.query(GroupModel.group_name).filter(GroupModel.group_id == group_id).scalar()
    session.query(StudentModel).filter(StudentModel.group_name == group_name).update({"group_name": None})
    session.commit()
    group = session.query(GroupModel).filter(GroupModel.group_id == group_id).first()
    session.delete(group)
    session.commit()
    return group_id, group_name


def get_groups():
    groups = session.query(GroupModel).all()
    result = [{'group_id': group.group_id, 'group_name': group.group_name} for group in groups]
    return result


def add_group_to_table(group_id, group_name):
    new_group = GroupModel(group_id=group_id, group_name=group_name)
    session.add(new_group)
    session.commit()
    return group_id, group_name


def get_course_by_id(course_id):
    course = session.query(CourseModel).filter(CourseModel.course_id == course_id).first()
    return course.course_id, course.course_name, course.description


def delete_course(course_id):
    course_name = session.query(CourseModel.course_name).filter(CourseModel.course_id == course_id).scalar()
    course = session.query(CourseModel).filter(CourseModel.course_id == course_id).first()
    session.delete(course)
    session.commit()
    return course_id, course_name


def update_course(course_id, course_name):
    session.query(CourseModel).filter_by(course_id=course_id).update({'course_name': course_name})
    session.commit()
    return course_id, course_name


def get_courses():
    courses = session.query(CourseModel).all()
    result = [{'course_id':course[0], 'course_name': courses[1], 'description': course[2]} for course in courses]
    return result


def add_course_to_table(course_id, course_name, description):
    new_course = CourseModel(course_id=course_id, course_name=course_name, description=description)
    session.add(new_course)
    session.commit()
    return course_id, course_name


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


def delete_student_by_id(student_id):
    session.query(StudentCourse).filter(StudentCourse.student_id == student_id).delete()
    session.query(StudentModel).filter(StudentModel.student_id == student_id).delete()
    session.commit()
    return student_id


def add_student_to_course(student_id, course_name_list):
    student = session.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    for course_name in course_name_list:
        course = session.query(CourseModel).filter(CourseModel.course_name == course_name).first()

        student.add_course(course)
    session.commit()
    return student_id, course_name_list


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
    return student_id, course_name


