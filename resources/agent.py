import sqlite3
import os
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Agent(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('os', type=str, required=True)
    parser.add_argument('location', type=str, required=True)
    parser.add_argument('function', type=str, required=False)

    def get(self, hostname):
        agent = next(
            filter(lambda x: safe_str_cmp(x['hostname'], hostname), agents),
            None)
        return {'agent': agent}, 200 if agent else 404

    def post(self, hostname):
        if next(filter(lambda x: x['hostname'] == hostname, agents), None):
            return {
                'message':
                "An agent with hostname  '{}' already exists.".format(hostname)
            }, 404
        data = Agent.parser.parse_args()
        agent = {
            'hostname': hostname,
            'os': data['os'],
            'location': data['location']
        }
        agents.append(agent)
        return agent, 201

    def delete(self, hostname):
        global agents
        agents = list(filter(lambda x: x['hostname'] != hostname, agents))
        return {'message': 'Agent deleted'}

    def put(self, hostname):
        data = Agent.parser.parse_args()
        agent = next(
            filter(lambda x: safe_str_cmp(x['hostname'], hostname), agents),
            None)
        if agent == None:
            agent = {
                'hostname': hostname,
                'os': data['os'],
                'location': data['location']
            }
            agents.append(agent)
        else:
            agent.update(data)
        return agent


class AgentList(Resource):
    def get(self):
        conn = sqlite3.connect(os.path.join('..', 'db', 'servers.db'))
        cursor = conn.cursor()

        result = cursor.execute(
            'SELECT agentName, os, location, function FROM agents')
        servers = []
        for row in result:
            servers.append({
                'agentName': row[0],
                'os': row[1],
                'location': row[2],
                'function': row[3]
            })
        conn.commit()
        conn.close()
