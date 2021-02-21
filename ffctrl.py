import json
import socket


# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   https://github.com/nneonneo/2048-ai
# Description: Handles the communication with the firefox browser.

class FirefoxRemoteControl(object):
    ''' Interact with a web browser running the Remote Control extension. '''

    def __init__(self, port):
        self.sock = socket.socket()
        self.sock.connect(('localhost', port))

    def execute(self, cmd):
        msg = cmd.replace('\n', ' ') + '\r\n'
        self.sock.send(msg.encode('utf8'))
        ret = []
        while True:
            chunk = self.sock.recv(4096)
            ret.append(chunk)
            if b'\n' in chunk:
                break
        res = json.loads(b''.join(ret).decode('utf8'))
        if 'error' in res:
            raise Exception(res['error'])
        elif not res:
            return None
        else:
            return res['result']
