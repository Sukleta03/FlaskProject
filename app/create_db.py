
def init_db(engine):
    from app.models import Base

    Base.metadata.create_all(bind=engine)


