from db import db


class ServerModel(db.Model):
    __tablename__ = 'servers_inventory'

    serverName = db.Column(db.String(50), primary_key=True)
    enabled = db.Column(db.Boolean)
    os = db.Column(db.String(10))
    location = db.Column(db.String(3))
    scope = db.Column(db.String(10))

    agentName = db.Column(db.String(50), db.ForeignKey('agents.agentName'))
    agent = db.relationship('AgentModel')

    def __init__(self, serverName, agentName, enabled, os, location, scope):
        self.serverName = serverName
        self.agentName = agentName
        self.enabled = enabled
        self.os = os
        self.location = location
        self.scope = scope

    def json(self):
        return {
            'serverName': self.serverName,
            'agentName': self.agentName,
            'enabled': self.enabled,
            'os': self.os,
            'location': self.location,
            'scope': self.scope
        }

    @classmethod
    def find_by_name(cls, hostname):
        return cls.query.filter_by(serverName=hostname).first()

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
