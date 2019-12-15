#!/usr/bin/env python3

import socket
import select
from neopixel import *
import argparse
import pickle
import time
import threading
class SocketServer(threading.Thread):
    """ Simple socket server that listens to one single client. """
    def __init__(self,strip, host = '0.0.0.0', port = 2010, *args, **kwargs):
        super(SocketServer, self).__init__(*args, **kwargs)
        self._stopp = threading.Event()
        """ Initialize the server with a host and port to listen to. """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.sock.bind((host, port))
        self.sock.listen(1)
        self.read_list = [self.sock]
        self.strip = strip

    def stopit(self):
        self._stopp.set()

    def stopped(self):
        return self._stopp.isSet()

    def stripColorSet(self, color):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def run(self):
        """ Accept and handle an incoming connection. """
        print('Starting socket server (host {}, port {})'.format(self.host, self.port))
        client_sock = None
        while True:
            if self.stopped():
                print("close socket server")
                if client_sock:
                    try:
                        client_sock.close()
                        self.read_list.remove(client_sock)
                    except:
                        pass
                self.sock.close()
                self.stripColorSet(Color(0,0,0))
                print("done closing")
                return
            readable, writable, errored = select.select(self.read_list, [], [], 1)
            for s in readable:
                if s is self.sock:
                    client_sock, client_addr = self.sock.accept()
                    self.read_list.append(client_sock)
                else:
                    data = client_sock.recv(255)
                    if data:
                        try:
                            read_data= pickle.loads(data)
                        except:
                            read_data=[0,0,0]
                        color = Color(read_data[0], read_data[1], read_data[2])
                        self.stripColorSet(color)
                    else:
                        try:
                            client_sock.close()
                            self.read_list.remove(client_sock)
                        except:
                            pass
        self.stripColorSet(Color(0,0,0))
#        return 0

#continu=True
#while continu:
#    try:
#        server = SocketServer()
#        server.run_server()
#        continu = True
#    except KeyboardInterrupt:
#        server.close()
#        continu = False
