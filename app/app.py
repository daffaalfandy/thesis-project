import os
import random
import string
from flask import Flask, request
import mysql.connector

WEBSERVER_IPADDR = "192.168.18.101"
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
        self.cursor.execute('CREATE TABLE client_access (id INT AUTO_INCREMENT PRIMARY KEY, ip_address VARCHAR(100), random_str VARCHAR(100));')
        self.connection.commit()
        
    def insert_ip_addr(self, ip_addr, random_str):
        self.cursor.execute("INSERT INTO client_access (ip_address, random_str) VALUES ('{}', '{}');".format(ip_addr, random_str))
        self.connection.commit()
    

def eratosthenes(n):
    all = []
    prime = 1
    i = 3
    while (i <= n):
        if  i not in all:
            prime += 1
            j = i
            while (j <= (n / i)):
                all.append(i * j)
                j += 1
        i += 2
    
app = Flask(__name__)
conn = None

@app.route('/')
def home():
    ip_addr = request.remote_addr
    random_str = "".join((random.choice(string.ascii_uppercase) for x in range(90)))
    
    global conn
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
        conn.populate_db()
    
    conn.insert_ip_addr(ip_addr, random_str)
    
    eratosthenes(1000)
    
    response = '<h1> Client with IP Address: {} </h1>'.format(ip_addr)
    response += '</br> <h1> Have a random string: {} </h1>'.format(random_str)
    response += '</br> <strong> <h2> Served by Server with IP Addreess: {} </h2> </strong>'.format(WEBSERVER_IPADDR)
    
    return response