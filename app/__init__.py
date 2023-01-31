from flask import Flask

from app.models import StudentModel, Session, GroupModel


def create_app():
    app = Flask(__name__)

    from config import MainConfig
    app.config.from_object(MainConfig)

    from sqlalchemy import create_engine
    from app.create_db import init_db
    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    engine = create_engine(db_url, echo=True)
    init_db(engine)

    from app.create_models import fill_data
    try:
        fill_data(engine)
    except:
        pass

    from app.view import pages_blueprint
    app.register_blueprint(pages_blueprint)
    return app
