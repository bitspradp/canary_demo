#!/usr/bin/env python
from version import *
from random import randrange
from flask import Flask
from prometheus_client import start_http_server, Counter
import os
import time
import socket

app = Flask('kayenta-tester')
c = Counter('requests', 'Number of requests served, by http code', ['http_code'])

@app.route('/healthz')
def healthz():
    return 'Healthy\n'

@app.route("/disp")
def disp():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        return "HOST_NAME: "+host_name+" IP_ADDRESS: "+host_ip+" DEPLOYMENT_VERSION: "+version+"\n"
    except:
        return "Unable to serve requests presently\n"

@app.route('/hello')
def hello():
    if randrange(1, 100) > int(os.environ['SUCCESS_RATE']):
        c.labels(http_code = '500').inc()
        return "Internal Server Error\n", 500
    else:
        c.labels(http_code = '200').inc()
        return "Hello World!\n"

start_http_server(6000)
app.run(host = '0.0.0.0', port = 5000)
