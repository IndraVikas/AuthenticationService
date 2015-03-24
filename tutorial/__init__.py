import os

from pyramid.config import Configurator
from models.auth import DBSession, Base
from sqlalchemy import create_engine

#from scripts.initializedb import get_db_connection_dict, DB_FORMAT_STRING

DB_FORMAT_STRING = 'postgresql://{user}:{password}@{host}:{port}/{db_name}'

def get_db_connection_dict():
    """
    Build a dict of connection arguments from the environment.

    :return:
    """
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    return dict(
        db_name=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=DB_HOST,
        port=DB_PORT,
        )


def main(global_config, **settings):
    db_kwargs = get_db_connection_dict()
    engine = create_engine(DB_FORMAT_STRING.format(**db_kwargs))
    print "Engine created "+ DB_FORMAT_STRING.format(**db_kwargs)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')
    config.include('pyramid_chameleon')
    config.scan('.views')
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('signin', '/signin')
    return config.make_wsgi_app()
