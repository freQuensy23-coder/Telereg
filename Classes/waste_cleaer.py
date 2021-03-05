from Classes.request import TTL, Request
from time import time


class Waste_cleaner:
    """Removes old requests records"""
    def __init__(self, session):
        self.session = session

    def clean(self):
        t = time()
        requests = self.session.query(Request).filter(Request.created > TTL + t).all()
        for request in requests:
            print(request)
            self.session.delete(request)

        self.session.commit()