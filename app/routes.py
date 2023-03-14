from flask import request
from flask_restful import Api, Resource
from app.orm_querys import get_groups_with_less_students_count, \
    students_from_course_by_name, \
    add_student_to_table, \
    delete_student_by_id, \
    add_student_to_course, delete_student_from_course


class GroupsLessThenCount(Resource):
    def get(self):
        max_student_in_group = request.args.get('student_count')
        result = get_groups_with_less_students_count(max_student_in_group)
        data = [{'group_name': row[0], 'student_count': row[1]} for row in result]
        return data


class StudentsFromCourse(Resource):
    def get(self):
        course_name = request.args.get('course_name')
        result = students_from_course_by_name(course_name)
        data = [{'first_name': row[0], 'last_name': row[1], 'course_name': row[2]} for row in result]
        return data


class DeleteStudent(Resource):
    def get(self):
        student_id = request.args.get('student_id')
        result = delete_student_by_id(student_id)
        return {result: 'Was deleted'}


class AddStudent(Resource):
    def get(self):
        student_id = request.args.get('student_id')
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        group_name = request.args.get('group_name')
        try:
            result = add_student_to_table(student_id, first_name, last_name, group_name)
            return {'new_student': result}
        except:
            return {'new_student': 'Is already exist or validation failed'}


class AddStudentToCourse(Resource):
    def get(self):
        student_id = request.args.get('student_id')
        course_name = request.args.get('course_name').split(' ')
        result = add_student_to_course(student_id, course_name)
        return {result[0]: [course for course in result[1]]}


class DeleteFromCourse(Resource):
    def get(self):
        from app.orm_querys import session

        student_id = request.args.get('student_id')
        course_name = request.args.get('course_name')
        result = delete_student_from_course(session, student_id, course_name)
        return {result[0]: result[1]}


api = Api()
api.add_resource(GroupsLessThenCount, '/groups')
api.add_resource(StudentsFromCourse, '/students')
api.add_resource(DeleteStudent, '/delete')
api.add_resource(AddStudent, '/add')
api.add_resource(AddStudentToCourse, '/add_to_course')
api.add_resource(DeleteFromCourse, '/delete_from_course')

