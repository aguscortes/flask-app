import sqlite3, os
from flask_restful import Resource, reqparse
from models.server import ServerModel


class Server(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('os', type=str, required=False)
    parser.add_argument('location', type=str, required=False)
    parser.add_argument('agent', type=str, required=True)

    def get(self, hostname):
        server = ServerModel.find_by_name(hostname)
        if server:
            return server.json()
        return {'message': 'Server not found'}, 400

    def post(self, hostname):
        if ServerModel.find_by_name(hostname):
            return {
                'message':
                "A server with hostname  '{}' already exists.".format(hostname)
            }, 400

        data = Server.parser.parse_args()
        server = ServerModel(hostname, **data)
        try:
            server.add_to_db()
        except:
            return {'message': 'An error occurred inserting the server'}, 500
        return server.json(), 201

    def delete(self, hostname):
        server = Server.find_by_name(hostname)
        if server:
            server.delete_from_db()
        return {'message': 'Server deleted'}

    def put(self, hostname):
        data = Server.parser.parse_args()

        server = Server.find_by_name(hostname)

        if server is None:
            server = ServerModel(hostname, **data)
        else:
            server.agentName = data['agentName']
            server.enabled = data['enabled']
            server.os = data['os']
            server.location = data['location']
            server.scope = data['scope']
        server.add_to_db()
        return server.json()


class ServerList(Resource):
    def get(self):
        return {'servers': [x.json() for x in ServerModel.query.all()]}
