import os
import sys

import transaction
from sqlalchemy import create_engine
from quick_tutorial.login.tutorial.models.auth import (
    DBSession,
    User,
    Base,
    )


DB_FORMAT_STRING = 'postgresql://{user}:{password}@{host}:{port}/{db_name}'

def get_db_connection_dict():
    """
    Build a dict of connection arguments from the environment.

    :return:
    """
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')

    return dict(
        db_name=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=DB_HOST,
        port=DB_PORT,
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    db_kwargs = get_db_connection_dict()
    engine = create_engine(DB_FORMAT_STRING.format(**db_kwargs))
    print "++++++++++++++++++"+DB_FORMAT_STRING.format(**db_kwargs)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    print "hello world.------------------"
    with transaction.manager:
        user = User("indra", "password",)
        print 'user created.--------------------'
        DBSession.add(user)