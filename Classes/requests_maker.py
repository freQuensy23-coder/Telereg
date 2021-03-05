import uuid

from sqlalchemy.orm import session as sql_session
from random import randint
from Classes.request import Request

from time import time

from status import *


class Requests_maker:
    def __init__(self, session: sql_session):
        self.session = session

    def create_req(self):
        r = Request(r_key=self.__generate_r_key(),
                    code=self.__generate_code(),
                    created=int(time()),
                    status=status_encode("wait"))
        return r

    def __generate_code(self):
        """Generate random uniq code"""
        code = randint(10000, 99999) # TODO
        while self.session.query(Request).filter_by(code = code).first() is not None: # If code was not uniq
            code = randint(10000, 99999)
        return code

    def __generate_r_key(self):
        r_key = str(uuid.uuid4())
        while self.session.query(Request).filter_by(r_key = r_key).first() is not None: # If r_key was not uniq
            r_key = str(uuid.uuid4())
        return r_key
