from mock import patch
from app import create_app
import pytest


class TestApi:
    @pytest.fixture()
    def app(self):
        app = create_app('test')
        return app

    @patch('app.routes.get_student')
    def test_student_request(self, mock_response_func, client):
        mock_response_func.return_value = ['255', 'Dima', 'Sukleta', 'PE-21']
        response = client.get('/api/v1/student/255')
        assert response.status_code == 200
        assert {'student_id': '255', 'first_name': 'Dima', 'last_name': 'Sukleta', 'group_name': 'PE-21'} == response.json

    @patch('app.routes.update_student')
    def test_student_update(self, mock_response_func, client):
        mock_response_func.return_value = ['255', 'Dima', 'Sukleta', 'PE-21']
        response = client.put('/api/v1/student/255?first_name=Dima&last_name=Sukleta&group_name=PE-21')
        assert response.status_code == 200
        assert {'updated_student': ['255', 'Dima', 'Sukleta', 'PE-21']} == response.json

    @patch('app.routes.delete_student_by_id')
    def test_student_delete(self, mock_response_func, client):
        mock_response_func.return_value = 255
        response = client.delete('/api/v1/student/255')
        assert response.status_code == 200
        assert {'255': 'Was deleted'} == response.json

    @patch('app.routes.get_students')
    def test_students_request(self, mock_response_func, client):
        mock_response_func.return_value = [{'student_id': 255, 'first_name': 'Dima', 'last_name': 'Sukleta', 'group_name': 'PE-21'}]
        response = client.get('/api/v1/students')
        assert response.status_code == 200
        assert [{'student_id': 255, 'first_name': 'Dima', 'last_name': 'Sukleta', 'group_name': 'PE-21'}] == response.json

    @patch('app.routes.add_student_to_table')
    def test_student_add(self, mock_response_func, client):
        mock_response_func.return_value = ['255', 'Dima', 'Sukleta', 'PE-21']
        response = client.post('/api/v1/students?student_id=255&first_name=Dima&last_name=Sukleta&group_name=PE-21')
        assert response.status_code == 200
        assert {'new_student': ['255', 'Dima', 'Sukleta', 'PE-21']} == response.json

    @patch('app.routes.get_group')
    def test_group_request(self, mock_response_func, client):
        mock_response_func.return_value = ['1', 'PE-21']
        response = client.get('/api/v1/group/1')
        assert response.status_code == 200
        assert {'group_id': '1', 'group_name': 'PE-21'} == response.json

    @patch('app.routes.update_group')
    def test_group_update(self, mock_response_func, client):
        mock_response_func.return_value = ['1', 'PE-21']
        response = client.put('/api/v1/group/1?group_name=PE-21')
        assert response.status_code == 200
        assert {'updated_group': ['1', 'PE-21']} == response.json

    @patch('app.routes.delete_group_by_id')
    def test_group_delete(self, mock_response_func, client):
        mock_response_func.return_value = [1, 'PE-21']
        response = client.delete('/api/v1/group/1')
        assert response.status_code == 200
        assert {'PE-21': 'Was deleted'} == response.json

    @patch('app.routes.get_groups')
    def test_groups_request(self, mock_response_func, client):
        mock_response_func.return_value = [{'group_id': 1, 'group_name': 'PE-21'}]
        response = client.get('/api/v1/groups')
        assert response.status_code == 200
        assert [{'group_id': 1, 'group_name': 'PE-21'}] == response.json

    @patch('app.routes.get_groups_with_less_students_count')
    def test_groups_request_2(self, mock_response_func, client):
        mock_response_func.return_value = [{'group_name': 'PE-21', 'student_count': 14}]
        response = client.get('/api/v1/groups/15')
        assert response.status_code == 200
        assert [{'group_name': 'PE-21', 'student_count': 14}] == response.json

    @patch('app.routes.add_group_to_table')
    def test_group_add(self, mock_response_func, client):
        mock_response_func.return_value = ['1', 'PE-21']
        response = client.post('/api/v1/groups?group_id=1&group_name=PE-21')
        assert response.status_code == 200
        assert {'new_group': ['1', 'PE-21']} == response.json

    @patch('app.routes.get_course_by_id')
    def test_course_request(self, mock_response_func, client):
        mock_response_func.return_value = ['1', 'Math', 'description will be soon']
        response = client.get('/api/v1/course/1')
        assert response.status_code == 200
        assert {'course_name': 'Math', 'description': 'description will be soon'} == response.json

    @patch('app.routes.update_course')
    def test_course_update(self, mock_response_func, client):
        mock_response_func.return_value = ['1', 'Math']
        response = client.put('/api/v1/course/1?course_name=Math')
        assert response.status_code == 200
        assert {'updated_course': 'Math'} == response.json

    @patch('app.routes.delete_course')
    def test_course_delete(self, mock_response_func, client):
        mock_response_func.return_value = [1, 'Math']
        response = client.delete('/api/v1/course/1')
        assert response.status_code == 200
        assert {'Math': 'Was deleted'} == response.json

    @patch('app.routes.get_courses')
    def test_courses_request(self, mock_response_func, client):
        mock_response_func.return_value = [{'course_id': 1, 'course_name': 'Math', 'description': 'description will be soon'}]
        response = client.get('/api/v1/courses')
        assert response.status_code == 200
        assert [{'course_id': 1, 'course_name': 'Math', 'description': 'description will be soon'}] == response.json

    @patch('app.routes.add_course_to_table')
    def test_course_add(self, mock_response_func, client):
        mock_response_func.return_value = ['1', 'Math']
        response = client.post('/api/v1/courses?course_id=1&course_name=Math&description=description+will+be+soon')
        assert response.status_code == 200
        assert {'new_course': ['1', 'Math']} == response.json

    @patch('app.routes.students_from_course')
    def test_students_by_course_request(self, mock_response_func, client):
        mock_response_func.return_value = [('Dima', 'Sukleta', 'Math')]
        response = client.get('/api/v1/course/1/students')
        assert response.status_code == 200
        assert [{'first_name': 'Dima', 'last_name': 'Sukleta', 'course_name': 'Math'}] == response.json

    @patch('app.routes.add_student_to_course')
    def test_add_to_course(self, mock_response, client):
        mock_response.return_value = ('255', ['Math', 'English'])
        response = client.put('/api/v1/course/students?student_id=199&course_name=Math+English')
        assert response.status_code == 200
        assert {'255': ['Math', 'English']} == response.json

    @patch('app.routes.delete_student_from_course')
    def test_delete_from_course(self, mock_response, client):
        mock_response.return_value = ('255', 'Math')
        response = client.delete('/api/v1/course/1/students/255')
        assert response.status_code == 200
        assert {'255': 'Math'} == response.json

