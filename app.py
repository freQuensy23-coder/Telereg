
from flask import Flask, send_file, jsonify, request
from flask_restful import Api, Resource, reqparse

from Classes.requests_maker import Requests_maker

from requests_database import session

from Classes.request import Request

from Classes.waste_cleaer import Waste_cleaner

app = Flask("Test")
api = Api(app)


class Create_new_req(Resource):
    def post(self):
        r = requests_maker.create_req()
        session.add(r)
        session.commit()
        return r.jsonify()


class Get_req_status(Resource):
    def get(self, key):
        r = session.query(Request).filter_by(r_key=key).first()
        print(r.jsonify())
        waste_cleaner.clean()
        return r.jsonify()


if __name__ == '__main__':
    waste_cleaner = Waste_cleaner(session=session)
    requests_maker = Requests_maker(session=session)
    api.add_resource(Create_new_req, "/new")
    api.add_resource(Get_req_status, "/requests/<string:key>")
    app.run(debug=True, host="localhost", port=122)
