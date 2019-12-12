#!/usr/bin/env python3

import socket
import select
from neopixel import *
import argparse
import pickle


# LED strip configuration:
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.SK6812W_STRIP
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

class SocketServer:
    """ Simple socket server that listens to one single client. """
    def __init__(self, host = '0.0.0.0', port = 2010):
        """ Initialize the server with a host and port to listen to. """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.sock.bind((host, port))
        self.sock.listen(1)

    def stripColorSet(self, color):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            strip.setPixelColor(i, color)
        strip.show()
    def close(self):
        """ Close the server socket. """
        print('Closing server socket (host {}, port {})'.format(self.host, self.port))
        if self.sock:
            self.sock.close()
            self.sock = None
        self.stripColorSet(Color(0,0,0))

    def run_server(self):
        """ Accept and handle an incoming connection. """
        print('Starting socket server (host {}, port {})'.format(self.host, self.port))

        client_sock, client_addr = self.sock.accept()

        print('Client {} connected'.format(client_addr))

        stop = False
        red = 0
        green = 0
        blue = 0
        while not stop:
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
        self.stripColorSet(Color(0,0,0))
        return 0

continu=True
while continu:
    try:
        server = SocketServer()
        server.run_server()
        continu = True
    except KeyboardInterrupt:
        server.close()
        continu = False
