from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from werkzeug.security import safe_str_cmp

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = '1234'
api = Api(app)

jwt = JWT(app, authenticate, identity)

servers = []
agents = []

class Agent(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('so', type=text, required=True)
	parser.add_argument('location', type=text, required=True)

	def get(self, hostname):
		agent = next(filter(lambda x: safe_str_cmp(x['hostname'], hostname), agents), None)
		return {'agent' : agent}, 200 if agent else 404

	@jwt_required()
	def post(self,hostname):
		if next(filter(lambda x: x['hostname'] == hostname, agents), None):
				return {'message' :"An agent with hostname  '{}' already exists.".format(hostname)}, 404
		data = Agent.parser.parse_args()
		agent = {'hostname': hostname , 'so' : data['so'], 'location' : data['location']}
		agents.append(agent)
		return agent, 201

	@jwt_required()
	def delete(self, hostname):
		global agents
		agents = list(filter(lambda x: x['hostname'] != hostname, agents))
		return {'message' : 'Agent deleted'}

	@jwt_required()
	def put (self, hostname):
		data = Agent.parser.parse_args()
		agent = next(filter(lambda x: safe_str_cmp(x['hostname'], hostname), agents), None)
		if agent == None:
			agent = {'hostname': hostname , 'so' : data['so'], 'location' : data['location']}
			agents.append(agent)
		else:
			agent.update(data)
		return agent


class AgentList(Resource):
	def get(self):
		return {'agents' : agents}


class Server(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('so', type=text, required=False)
	parser.add_argument('location', type=text, required=False)
	parser.add_argument('agent', type=text, required=True)

	def get(self, hostname):
		server = next(filter(lambda x: safe_str_cmp(x['hostname'], hostname), servers), None)
		return {'server' : server}, 200 if server else 404
	

	def post(self,hostname):
		if next(filter(lambda x: x['hostname'] == hostname, servers), None):
				return {'message' :"A server with hostname  '{}' already exists.".format(hostname)}, 404
		data = request.parser.parse_args()
		server = {'hostname': hostname , 
					'so' : data['so'], 
					'location' : data['location'],
					'agent' : data['agent']}
		servers.append(server)
		return server, 201


	def delete(self, hostname):
		global servers
		servers = list(filter(lambda x: x['hostname'] != hostname, servers))
		return {'message' : 'Server deleted'}


	def put (self, hostname):
		data = Server.parser.parse_args()
		server = next(filter(lambda x: safe_str_cmp(x['hostname'], hostname), servers), None)
		if server == None:
			server = {'hostname': hostname, 
					'so' : data['so'], 
					'location' : data['location'],
					'agent' : data['agent']}			
			servers.append(server)
		else:
			server.update(data)
		return server


class ServerList(Resource):
	def get(self):
		return {'servers' : servers}


api.add_resource(Agent, '/agent/<string:hostname>')
api.add_resource(Server, '/server/<string:hostname>')
api.add_resource(AgentList, '/agents')
api.add_resource(ServerList, '/servers')

app.run(port=5000, debug=True)