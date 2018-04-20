import sqlite3, os
from flask_restful import Resource, reqparse
from models.agent import AgentModel


class Agent(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('os', type=str, required=True)
    parser.add_argument('location', type=str, required=True)
    parser.add_argument('function', type=str, required=False)

    def get(self, hostname):
        agent = AgentModel.find_by_name(hostname)
        if agent:
            return agent.json()
        return {'message': 'Agent not found'}, 400

    def post(self, hostname):
        if AgentModel.find_by_name(hostname):
            return {
                'message':
                "An agent with hostname  '{}' already exists.".format(hostname)
            }, 404

        data = Agent.parser.parse_args()
        agent = AgentModel(hostname, **data)
        try:
            agent.add_to_db()
        except:
            return {'message': 'An error occurred inserting the agent'}, 500
        return agent.json(), 201

    def delete(self, hostname):
        agent = AgentModel.find_by_name(hostname)
        try:
            if agent:
                agent.delete_from_db()
        except:
            return {'message': 'An error occurred deleting the agent'}, 500
        return {'message': 'Agent deleted'}

    def put(self, hostname):
        data = Agent.parser.parse_args()
        agent = AgentModel.find_by_name(hostname)
        if agent is None:
            agent = AgentModel(hostname, **data)
        else:
            agent.os = data['os']
            agent.location = data['location']
            agent.scope = data['function']
        agent.add_to_db()
        return agent.json()


class AgentList(Resource):
    def get(self):
        return {'agents': [x.json() for x in AgentModel.query.all()]}
