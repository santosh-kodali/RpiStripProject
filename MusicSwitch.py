# An Accessory for viewing/controlling the status of a Mac display.
import subprocess

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SWITCH


class MusicStart(Accessory):
    """A switch accessory that executes start music script."""

    category = CATEGORY_SWITCH

    def __init__(self, *args, **kwargs):
        """Initialize and set a shutdown callback to the On characteristic."""
        super().__init__(*args, **kwargs)
        self.state = False
        self.process = None
        serv_switch = self.add_preload_service('Switch')
        self.display = serv_switch.configure_char(
            'On', setter_callback=self.execute_script)

    def execute_script(self, _value):
        """Execute sscript"""
        if self.state:
            if self.process:
                print('terminate')
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            self.state = False
        else:
            self.process = subprocess.Popen(['sudo', '/home/pi/myprojects/comms/socket2.py'], preexec_fn=$
            self.state=True
        self.display.value = self.state
        self.display.notify()
