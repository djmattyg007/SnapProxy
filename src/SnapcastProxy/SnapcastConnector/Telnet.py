import logging
import threading
import time
import telnetlib
from SnapcastProxy.EventManager.Events import Events
import json

class SnapTelnet():
    def __init__(self, eventmanager):
        threading.Thread.__init__(self)
        self.eventmanager = eventmanager
        self._logger = logging.getLogger(__name__)
        self.connection = telnetlib.Telnet('127.0.0.1', 1705)
        self.exit = False
        self.eventmanager.subscribe(Events.ON_TELNET_SEND, self._on_send)
        self._logger.info('Connected to Snapcast')

    def _on_send(self, mgr, message):
        self.send(json.loads(message))

    def send(self, jsonrpc):
        #jsonrpc = json.dumps(jsonrpc)
        self._logger.debug('Seding via Telnet: ' + jsonrpc)
        jsonrpc = jsonrpc.replace('\n', '')

        self.connection.write((jsonrpc + '\r\n').encode('ascii'))

    def listen(self):
        response = self.connection.read_until(('\r\n').encode(), 2)
        if response:
            self.eventmanager.publish(Events.ON_BROADCAST, response.rstrip())
            self._logger.debug('Receiving via Telnet: ' + response.rstrip().decode())
            return response

    def close(self):
        self.connection.close()

