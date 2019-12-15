# An Accessory for viewing/controlling the status of a Mac display.
import subprocess
import signal
from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SWITCH
import os
from socket2 import SocketServer

class MusicStart(Accessory):
    """A switch accessory that executes start music script."""

    category = CATEGORY_SWITCH

    def __init__(self,strip,*args, **kwargs):
        """Initialize and set a shutdown callback to the On characteristic."""
        super().__init__(*args, **kwargs)
        self.state = False
        self.process = None
        serv_switch = self.add_preload_service('Switch')
        self.display = serv_switch.configure_char(
            'On', setter_callback=self.execute_script)
        self.strip = strip
        self.t1 = None
    def execute_script(self, _value):
        """Execute sscript"""
        if self.state:
            print('call stop')
            self.t1.stopit()
            print('stopped')
#            self.t1.join()
            print('joined')
             #   os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            self.state = False
        else:
            #self.process = subprocess.Popen(['sudo', '/home/pi/myprojects/rpiAudioMain/socket2.py'], preexec_fn=os.setsid)
            self.t1 = SocketServer(self.strip)
            self.t1.start()
            self.state=True
        self.display.value = self.state
        self.display.notify()
