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
        self.strip = strip

    def stopit(self):
        self._stopp.set()
        #print(self._stop.isSet())

    def stopped(self):
        print(self._stopp.isSet())
        print("hi")
        return self._stopp.isSet()

    def stripColorSet(self, color):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
    def close(self):
        """ Close the server socket. """
        print('Closing server socket (host {}, port {})'.format(self.host, self.port))
        if self.sock:
            self.sock.close()
            self.sock = None
        self.stripColorSet(Color(0,0,0))

    def run(self):
        """ Accept and handle an incoming connection. """
        print('Starting socket server (host {}, port {})'.format(self.host, self.port))

        client_sock, client_addr = self.sock.accept()

        print('Client {} connected'.format(client_addr))

        stop = False
        red = 0
        green = 0
        blue = 0
        while True:
            if self.stopped():
                return
            if stop:
                return
            if client_sock:
                # Check if the client is still connected and if data is available:
                try:
                    rdy_read, rdy_write, sock_err = select.select([client_sock,], [], [])
                except select.error:
       	            print('Select() failed on socket with {}'.format(client_addr))
                    return 1

                if len(rdy_read) > 0:
                    read_data = client_sock.recv(255)
                    # Check if socket has been closed
                    if len(read_data) == 0:
                        print('{} closed the socket.'.format(client_addr))
                        stop = True
                    else:
                        try:
                            read_data= pickle.loads(read_data)
                        except:
                            pass
                        color = Color(read_data[0], read_data[1], read_data[2])
                        self.stripColorSet(color)
                        #if read_data.rstrip() == 'quit':
                        #    stop = True
                        #else:
                        #    client_sock.send(read_data.encode())
            else:
                print("No client is connected, SocketServer can't receive data")
                stop = True

        # Close socket
        print('Closing connection with {}'.format(client_addr))
        client_sock.close()
        self.sock = None
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
