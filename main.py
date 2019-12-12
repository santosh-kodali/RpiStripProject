#!/usr/bin/env python3
"""An example of how to setup and start an Accessory.

This is:
1. Create the Accessory object you want.
2. Add it to an AccessoryDriver, which will advertise it on the local network,
    setup a server to answer client queries, etc.
"""
import logging
import signal
import random
import subprocess
import os
from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
#import pyhap.loader as loader
#from pyhap import camera
from MusicStart import MusicStart

logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")

def get_bridge(driver):
    """Call this method to get a Bridge instead of a standalone accessory."""
    bridge = Bridge(driver, 'Bridge')
    music_dis = MusicStart(driver, 'MusicDisplay')
    bridge.add_accessory(music_dis)
    return bridge


# Start the accessory on port 51828
driver = AccessoryDriver(port=51828, persist_file='main.state')

# Change `get_accessory` to `get_bridge` if you want to run a Bridge.
driver.add_accessory(accessory=get_bridge(driver))

# We want SIGTERM (terminate) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGTERM, driver.signal_handler)

# Start it!
driver.start()
