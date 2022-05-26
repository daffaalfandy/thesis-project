import os
from flask import Flask, request
import mysql.connector

class DBManager:
    def __init__(self, password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user='root',
            password=pf.read(),
            host='db',
            database='thesis',            
        )
        pf.close()
        self.cursor = self.connection.cursor()
        
    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS client_access;')
        self.cursor.execute('CREATE TABLE client_access (id INT AUTO_INCREMENT PRIMARY KEY, ip_address VARCHAR(100));')
        self.connection.commit()
        
    def insert_ip_addr(self, ip_addr):
        self.cursor.execute("INSERT INTO client_access (ip_address) VALUES ('{}');".format(ip_addr))
        self.connection.commit()
    
    
server = Flask(__name__)
conn = None

@server.route('/')
def home():
    ip_addr = request.remote_addr    
    
    global conn
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
        conn.populate_db()
    
    conn.insert_ip_addr(ip_addr)
    
    response = '<h1> Client with IP Address: {} </h1>'.format(ip_addr)
    
    return response


if __name__ == '__main__':
    server.run(debug=True)