from SnapcastProxy.Webserver.RequestHandler.BaseHandler import BaseHandler
from SnapcastProxy.EventManager.Events import Events
from SnapcastProxy.SnapcastConnector.Telnet import SnapTelnet
import logging
import logging.handlers
import json
import time
import tornado

class JSONrpcHandler(BaseHandler):

    def initialize(self, *args, **kwargs):
        self._logger = logging.getLogger(__name__)
        self.done = False
        self.eventmanager = kwargs.get('eventmanager')
        self.snapcast_connector = SnapTelnet(self.eventmanager)

        self.request_id = 0
        self.response = None
        self.response_available = False

    def post(self, *args, **kwargs):
        rpcrequest = json.loads(self.request.body.decode())
        self.request_id = rpcrequest['id']
        self._logger.debug(self.request.body.decode())
        self.snapcast_connector.send(self.request.body.decode())
        self.wait_for_telnet()
        self._logger.debug('Send via HTTP: ' + str(self.response.strip()))
        self.write(self.response)

    def wait_for_telnet(self):
        self.done = False
        while (not self.done):
            _response = self.snapcast_connector.listen()
            if (_response):
                print(_response)
                if 'id' in _response.decode() and json.loads(_response.decode())['id'] == self.request_id:
                    self.response = _response
                    self.done = True
