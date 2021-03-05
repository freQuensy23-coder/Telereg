from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker

from Classes.request import base, Request

engine = create_engine("sqlite:///database.db", echo = True)
base.metadata.create_all(engine)

Session_m = sessionmaker(bind=engine)
session = scoped_session(Session_m)
