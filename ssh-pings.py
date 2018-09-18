#!/usr/bin/env python3

import subprocess
import json
import re
import time
from operator import attrgetter

from flask import Flask, Response, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import ping

# journalctl -b -o json-pretty --since "-1h" -u ssh.service

app = Flask('ssh-pings-backend')
limiter = Limiter(app, key_func=get_remote_address, default_limits=["2 per second"])

def get_pings(since):
    pings = []
    pattern = re.compile('Failed password for [invalid user ]*root from ([^ ]+) port [0-9]+ .*')

    p = subprocess.Popen(['journalctl', '-b', '-o', 'json', '--since', since, '-u', 'sshd.service'], stdout=subprocess.PIPE)
    out = p.communicate()[0].decode('utf-8').strip()
    for log in out.split('\n'):
        if log != '':
            j = json.loads(log)

            m = pattern.match(j['MESSAGE'])
            if m != None:
                pings.append(ping.Ping(j['__REALTIME_TIMESTAMP'], m.group(1)))

    return pings

def last_ping():
    pings = get_pings('-1h')
    if len(pings) == 0:
        return ping.Ping()
    
    return max(pings, key=attrgetter('timestamp'))

@app.route('/last')
def ping_last():
    response = None

    p = last_ping()

    origin_location = p.origin_location()
    if origin_location is None:
        origin_location = "unknown"

    response = Response(json.dumps(p, cls=ping.PingEncoder))

    response.mimetype = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/since/<timestamp>')
def ping_since(timestamp):
    response = None

    try:
        timestamp = int(timestamp)
    except ValueError:
        response = Response(json.dumps({
            'error': 'Invalid timestamp! Expected time since epoch in µs'
        }))

        response.mimetype = 'application/json'
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    if time.time() * 1e6 - timestamp > 3600000000:
        response = Response(json.dumps({
            'error': 'Invalid timestamp! Can only be one hour before current time'
        }))
    else:
        pings = get_pings('@' + str(float(timestamp / float(1e6))))
        response = Response(json.dumps({
            'pings': pings
        }, cls=ping.PingEncoder))

    response.mimetype = 'application/json'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run('192.168.1.11')
