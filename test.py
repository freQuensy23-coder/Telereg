import unittest
from unittest import TestCase
from Classes.requests_maker import Requests_maker
from requests_database import session

class Tester(TestCase):
    def setUp(self) -> None:
        self.req_maker = Requests_maker(session=session)

    def test_create_req(self):
        r = self.req_maker.create_req()
        print(r.jsonify())