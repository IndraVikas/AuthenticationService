from tutorial.models.auth import (
    DBSession,
    User,
    Base,
    )
import transaction


class UserQuery():
    @staticmethod
    def add_user(user):
        with transaction.manager:
            DBSession.add(user)
            transaction.commit()
    @staticmethod
    def get_user(email_id):
        return DBSession.query(User).filter(User.email_id == email_id).first()

    def is_email_id_already_registered(self, email_id):
        if self.get_user(email_id) is not None:
            return True
        else:
            return False