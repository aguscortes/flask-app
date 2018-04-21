from flask import Flask
from flask_restful import Api
import os

from resources.agent import Agent, AgentList
from resources.server import Server, ServerList

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('.', 'db' , 'test.db')
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Agent, '/agent/<string:hostname>')
api.add_resource(Server, '/server/<string:hostname>')
api.add_resource(AgentList, '/agents')
api.add_resource(ServerList, '/servers')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000)
