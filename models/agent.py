import sqlite3, os
from db import db


class AgentModel(db.Model):
    __tablename__ = 'agents'

    agentName = db.Column(db.String(50), primary_key=True)
    os = db.Column(db.String(10))
    location = db.Column(db.String(3))
    function = db.Column(db.String(10))

    servers = db.relationship('ServerModel', lazy='dynamic')

    def __init__(self, agentName, os, location, function):
        self.agentName = agentName
        self.os = os
        self.location = location
        self.function = function

    def json(self):
        return {
            'agentName': self.agentName,
            'os': self.os,
            'location': self.location,
            'function': self.function,
            'servers': [server.json() for server in self.servers.all()]
        }

    @classmethod
    def find_by_name(cls, hostname):
        return cls.query.filter_by(agentName=hostname).first()

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
