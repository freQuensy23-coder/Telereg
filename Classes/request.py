from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from status import status_decode

base = declarative_base()

TTL = 15


class Request(base):
    __tablename__ = "requests"
    r_id = Column(Integer, primary_key=True)
    r_key = Column(String)
    code = Column(Integer)
    created = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return f"{self.r_id}, {self.r_key}, {self.code}, {self.created}, {self.status}"

    def jsonify(self) -> dict:
        return {"r_key": self.r_key,
                "code": self.code,
                "created": self.created,
                "TTl": TTL,
                "status": status_decode(self.status)}
