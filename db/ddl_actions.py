import sqlite3
import os

def create_servers_table():
    conn = sqlite3.connect(os.path.join('db','servers.db'))
    cursor = conn.cursor()
    # Drop the table if exists
    cursor.execute('''
        DROP TABLE IF EXISTS servers_inventory
        ''')    
    # Create the alarms table
    cursor.execute('''
        CREATE TABLE servers_inventory (
        serverName VARCHAR(50) PRIMARY KEY, 
        agentName VARCHAR(50),
        enabled BOOLEAN,
        os VARCHAR(10),
        location VARCHAR (3),
        scope VARCHAR(10)      
        )
        ''')
    # Create index
    cursor.execute('''
        CREATE UNIQUE INDEX idx_servers_serverName ON servers_inventory (serverName);  
        ''')    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()    

def create_agents_table():
    conn = sqlite3.connect(os.path.join('db','servers.db'))
    cursor = conn.cursor()
    # Drop the table if exists
    cursor.execute('''
        DROP TABLE IF EXISTS agents
        ''')    
    # Create the alarms table
    cursor.execute('''
        CREATE TABLE agents (
        agentName VARCHAR(50) PRIMARY KEY, 
        os VARCHAR(10),
        location VARCHAR (3),
        function VARCHAR (10)              
        )
        ''')
    # Create index
    cursor.execute('''
        CREATE UNIQUE INDEX idx_agents_agentName ON agents (agentName);  
        ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()    