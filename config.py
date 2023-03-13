class Base:
    pass


class TestConfig(Base):
    # test config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class MainConfig(Base):
    #main config
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:135636@localhost/postgres'
