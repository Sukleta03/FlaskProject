from flask import request
from flask_restful import Api, Resource
from app.orm_querys import get_student, \
    get_students, update_student, \
    get_group, update_group, delete_group_by_id,\
    get_groups, add_group_to_table,\
    get_course_by_id, update_course, delete_course, \
    get_courses, add_course_to_table, \
    get_groups_with_less_students_count, \
    students_from_course_by_name, \
    add_student_to_table, \
    delete_student_by_id, \
    add_student_to_course, delete_student_from_course


class Student(Resource):
    def get(self, student_id: int):
        data = get_student(student_id)
        return {'student_id': data[0], 'first_name': data[1], 'last_name': data[2], 'group_name': data[3]}

    def put(self, student_id: int):
        student_id = student_id
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        group_name = request.args.get('group_name')
        try:
            result = update_student(student_id, first_name, last_name, group_name)
            return {'updated_student': result}
        except:
            return {'updated_student': 'Is not exist or validation failed'}

    def delete(self, student_id: int):
        student_id = student_id
        result = delete_student_by_id(student_id)
        return {result: 'Was deleted'}


class Students(Resource):
    def get(self):
        result = get_students()
        return result

    def post(self):
        student_id = request.args.get('student_id')
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        group_name = request.args.get('group_name')
        try:
            result = add_student_to_table(student_id, first_name, last_name, group_name)
            return {'new_student': result}
        except:
            return {'new_student': 'Is already exist or validation failed'}


class Group(Resource):
    def get(self, group_id: int):
        group_id = group_id
        result = get_group(group_id)
        return {'group_id': result.group_id, 'group_name': result.group_name}

    def put(self, group_id: int):
        group_id = group_id
        group_name = request.args.get('group_name')
        try:
            result = update_group(group_id, group_name)
            return {'updated_group': result}
        except:
            return {'updated_group': 'Is not exist or validation failed'}

    def delete(self, group_id: int):
        group_id = group_id
        result = delete_group_by_id(group_id)
        return {result[1]: 'Was deleted'}


class Groups(Resource):
    def get(self):
        result = get_groups()
        return result

    def post(self):
        group_id = request.args.get('group_id')
        group_name = request.args.get('group_name')
        result = add_group_to_table(group_id, group_name)
        return {'new_group': result}


class Course(Resource):
    def get(self, course_id: int):
        course = get_course_by_id(course_id)
        return {'course_name': course[1], 'description': course[2]}

    def put(self, course_id: int):
        course_id = course_id
        course_name = request.args.get('course_name')
        course = update_course(course_id, course_name)
        return {'updated_course': course[1]}

    def delete(self, course_id: int):
        course_id = course_id
        result = delete_course(course_id)
        return {result[1]: 'Was deleted'}


class Courses(Resource):
    def get(self):
        result = get_courses()
        return result

    def post(self):
        course_id = request.args.get('course_id')
        course_name = request.args.get('course_name')
        description = request.args.get('description')
        result = add_course_to_table(course_id, course_name, description)
        return {'new_course': result}


class GroupWithLessStudents(Resource):
    def get(self):
        max_student_in_group = request.args.get('student_count')
        result = get_groups_with_less_students_count(max_student_in_group)
        data = [{'group_name': row[0], 'student_count': row[1]} for row in result]
        return data


class StudentCourse(Resource):
    def get(self):
        # get students by there course
        course_name = request.args.get('course_name')
        result = students_from_course_by_name(course_name)
        data = [{'first_name': row[0], 'last_name': row[1], 'course_name': row[2]} for row in result]
        return data

    def put(self):
        student_id = request.args.get('student_id')
        course_name = request.args.get('course_name').split(' ')
        result = add_student_to_course(student_id, course_name)
        return {result[0]: [course for course in result[1]]}

    def delete(self):
        from app.orm_querys import session

        student_id = request.args.get('student_id')
        course_name = request.args.get('course_name')
        result = delete_student_from_course(session, student_id, course_name)
        return {result[0]: result[1]}


api = Api()
api.add_resource(Student, '/api/v1/student/<int:student_id>')
api.add_resource(Students, '/api/v1/students')
api.add_resource(Group, '/api/v1/group/<int:group_id>')
api.add_resource(Groups, '/api/v1/groups')
api.add_resource(Course, '/api/v1/course/<int:course_id>')
api.add_resource(Courses, '/api/v1/courses')
api.add_resource(GroupWithLessStudents, '/api/v1/group_with_less_students')
api.add_resource(StudentCourse, '/api/v1/student_course')

