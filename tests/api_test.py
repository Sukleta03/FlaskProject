from mock import patch
from app import create_app
import pytest


class TestApi:
    @pytest.fixture()
    def app(self):
        app = create_app('test')
        return app

    @patch('app.routes.get_groups_with_less_students_count')
    def test_group_request(self, mock_response_func, client):
        mock_response_func.return_value = [('PE-21', 14)]
        response = client.get('/groups?student_count=15')
        assert response.status_code == 200
        assert [{'group_name': 'PE-21', 'student_count': 14}] == response.json

    @patch('app.routes.students_from_course_by_name')
    def test_students_request(self, mock_response_func, client):
        mock_response_func.return_value = [('Dima', 'Sukleta', 'Math')]
        response = client.get('/students?course_name=Math')
        assert response.status_code == 200
        assert [{'first_name': 'Dima', 'last_name': 'Sukleta', 'course_name': 'Math'}] == response.json

    def test_student_delete(self, client):
        response = client.get('/delete?student_id=255')
        assert response.status_code == 200
        assert {'255': 'Was deleted'} == response.json

    @patch('app.routes.add_student_to_table')
    def test_student_add(self, mock_response, client):
        mock_response.return_value = None
        response = client.get('/add?student_id=255&first_name=Dima&last_name=Sukleta&group_name=PE-21')
        assert response.status_code == 200
        assert {'new_student': ['255', 'Dima', 'Sukleta', 'PE-21']} == response.json

    @patch('app.routes.add_student_to_course')
    def test_add_to_course(self, mock_response, client):
        mock_response.return_value = None
        response = client.get('/add_to_course?student_id=255&course_name=Math+English')
        assert response.status_code == 200
        assert {'255': ['Math', 'English']} == response.json

    @patch('app.routes.delete_student_from_course')
    def test_delete_from_course(self, mock_response, client):
        mock_response.return_value = None
        response = client.get('/delete_from_course?student_id=255&course_name=Math')
        assert response.status_code == 200
        assert {'255': 'Math'} == response.json
