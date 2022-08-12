import socket
import random
import string
import json
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
    

def eratosthenes(num):
    prime_number = []
    prime = [True for i in range(num+1)]
    p = 2
    while (p * p <= num):
        if (prime[p] == True):
            for i in range(p * p, num+1, p):
                prime[i] = False
        p += 1

    for p in range(2, num+1):
        if prime[p]:
            prime_number.append(p)
    return prime_number
    
app = Flask(__name__)
conn = None

@app.route('/')
def home():
    hostname=socket.gethostname()
    server_ipaddr=socket.gethostbyname(hostname)
    ip_addr = request.remote_addr
    random_str = "".join((random.choice(string.ascii_uppercase) for x in range(90)))
    
    global conn
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
        conn.populate_db()
    
    conn.insert_ip_addr(ip_addr, random_str)
    
    prime_number = eratosthenes(1000)
    
    data = {
        "client_ipaddr": ip_addr,
        "served_by": hostname,
        "server_ipaddr": server_ipaddr,
        "random_str": random_str,
        "prime_number": prime_number
    }

    response = app.response_class(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )
    
    return response