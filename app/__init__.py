from flask import Flask


def create_app(config):
    app = Flask(__name__, instance_relative_config=False)

    if config == 'main':
        app.config.from_object('config.MainConfig')
    elif config == 'test':
        app.config.from_object('config.TestConfig')

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

    from app.routes import api
    api.init_app(app)

    return app
