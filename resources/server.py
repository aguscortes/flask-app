import sqlite3
import os
from flask_restful import Resource, reqparse


class Server(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('os', type=str, required=False)
    parser.add_argument('location', type=str, required=False)
    parser.add_argument('agent', type=str, required=True)

    @classmethod
    def find_by_name(cls, hostname):
        conn = sqlite3.connect(os.path.join('..', 'db', 'servers.db'))
        cursor = conn.cursor()
        row = cursor.execute(
            'SELECT * FROM servers_inventory  WHERE serverName LIKE ?',
            (hostname, )).fetchone()
        conn.close()
        if row:
            return {
                'server': {
                    'serverName': row[0],
                    'agentName': row[1],
                    'enabled': row[2],
                    'os': row[3],
                    'location': row[4]
                }
            }

    @classmethod
    def insert_new_server(cls, server):
        conn = sqlite3.connect(os.path.join('..', 'db', 'servers.db'))
        cursor = conn.cursor()

        result = cursor.execute('''
				INSERT OR IGNORE INTO servers_inventory (serverName, agentName, os, enabled, location, scope) 
				VALUES (?,?, ?, 1, ?, '')
				''', (server['serverName'], server['agentName'], server['os'],
          server['location']))

        conn.commit()
        conn.close()

    @classmethod
    def update_server(cls, server):
        conn = sqlite3.connect(os.path.join('..', 'db', 'servers.db'))
        cursor = conn.cursor()

        result = cursor.execute('''
						UPDATE servers_inventory  
						SET agentName = ?,
							os = ?,  
							location = ? 
						WHERE serverName LIKE ? 
						''', (server['agentName'], server['os'], server['location'],
            server['serverName']))

        conn.commit()
        conn.close()

    def get(self, hostname):
        try:
            server = self.find_by_name(hostname)
        except:
            return {'message': 'An error occurred searching the server'}, 500

        if server:
            return server
        return {'message': 'Server not found'}, 400

    def post(self, hostname):
        if self.find_by_name(hostname):
            return {
                'message':
                "A server with hostname  '{}' already exists.".format(hostname)
            }, 400

        data = Server.parser.parse_args()
        server = {
            'serverName': hostname,
            'agentName': data['agent'],
            'os': data['os'],
            'location': data['location']
        }

        try:
            self.insert_new_server(server)
        except:
            return {'message': 'An error occurred inserting the server'}, 500
        return server, 201

    def delete(self, hostname):
        try:
            conn = sqlite3.connect(os.path.join('..', 'db', 'servers.db'))
            cursor = conn.cursor()

            cursor.execute(
                'DELETE FROM servers_inventory WHERE serverName LIKE ?',
                (hostname, ))

            conn.commit()
            conn.close()
        except:
            return {'message': 'An error occurred deleting the server'}, 500
        return {'message': 'Server deleted'}

    def put(self, hostname):
        data = Server.parser.parse_args()
        server = {
            'serverName': hostname,
            'agentName': data['agent'],
            'os': data['os'],
            'location': data['location']
        }

        if self.find_by_name(hostname):
            try:
                self.update_server(server)
            except:
                return {
                    'message': 'An error occurred updating the server'
                }, 500
        else:
            try:
                self.insert_new_server(server)
            except:
                return {
                    'message': 'An error occurred inserting the server'
                }, 500
        return server


class ServerList(Resource):
    def get(self):
        conn = sqlite3.connect(os.path.join('..', 'db', 'servers.db'))
        cursor = conn.cursor()

        result = cursor.execute(
            'SELECT serverName, agentName, os, location FROM servers_inventory'
        )
        servers = []
        for row in result:
            servers.append({
                'serverName': row[0],
                'agentName': row[1],
                'os': row[2],
                'location': row[3]
            })
        conn.commit()
        conn.close()

        return {'servers': servers}
