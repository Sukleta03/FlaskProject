from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__, instance_relative_config=False)

    if config == 'main':
        app.config.from_object('config.MainConfig')
    elif config == 'test':
        app.config.from_object('config.TestConfig')

    db.init_app(app)
    with app.app_context():
        from app.create_models import fill_data
        from app.models import GroupModel, StudentModel, CourseModel, StudentCourse
        db.create_all()
        try:
            fill_data()
        except:
            pass

    from app.routes import api
    api.init_app(app)

    return app
