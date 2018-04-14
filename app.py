from flask import Flask
from flask_restful import Api

from resources.agent import Agent, AgentList
from resources.server import Server, ServerList

app = Flask(__name__)
api = Api(app)

api.add_resource(Agent, '/agent/<string:hostname>')
api.add_resource(Server, '/server/<string:hostname>')
api.add_resource(AgentList, '/agents')
api.add_resource(ServerList, '/servers')

if __name__ == '__main__':
	app.run(port=5000)