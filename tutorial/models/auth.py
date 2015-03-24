from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    Text,
    ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils.types.password import PasswordType

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    first_name = Column(Text)
    last_name = Column(Text)
    email_id = Column(Text, primary_key=True)
    user_category = Column(Text)
    password = Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
        ],
    ))
    is_active = Column(Boolean, default=True)

    def __init__(self, first_name, last_name, email_id, user_category, password, is_active=True):
        self.first_name = first_name
        self.last_name = last_name
        self.email_id = email_id
        self.user_category = user_category
        self.password = password
        self.is_active = is_active

    def check_password(self, input_password):
        '''Return True if we have a matching password'''
        return self.password == input_password













