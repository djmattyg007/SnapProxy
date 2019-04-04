import tornado.websocket
from tornado import gen, websocket, ioloop
import json
import sys
import logging
import traceback


from SnapcastProxy.EventManager.Events import Events
from SnapcastProxy.SnapcastConnector.Telnet import SnapTelnet

class WebSocketHandler(websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):

        self.eventManager = kwargs.pop('eventmanager')
        self.handlers = kwargs.pop('wshandlers')
        #self.eventManager.subscribe(Events.ON_BROADCAST, self.on_socket_broadcast)
        self.socket_open = False
        self._logger = logging.getLogger(__name__)
        self.snapcast_connector = None
        super(WebSocketHandler, self).__init__(*args, **kwargs)


    def check_origin(self, origin):
        return True

    def open(self):
        """
        initilized a new connection. here all config values etc. should be send to client
        """
        message = dict()
        message['client'] = self.request
        self.socket_open = True
        self.handlers.add(self)
        self._logger.info("New client connected")
        #self.eventManager.publish(Events.ON_CLIENT_CONNECTED, message)
        self.snapcast_connector = SnapTelnet(self.eventManager)


    def on_message(self, message):
        """
            handles incoming messages from browser and sends it to the bus
         """
        try:
            self.snapcast_connector.send(json.loads(message))
            #self.eventManager.publish(Events.ON_TELNET_SEND, message)

        except (RuntimeError, TypeError, NameError):
            traceback.print_exc(file=sys.stdout)
            self._logger.error("Runtime error in Websocket message handler")

    def on_close(self):
        """
        is called when a connection is closed. all connection based things should be cleanded here
        """
        self.socket_open = False
        #self.eventManager.unsubscribe(Events.ON_BROADCAST, self.on_socket_broadcast)
        #self.eventManager.unsubscribe(Events.ON_SOCKET_SEND, self.on_socket_send)
        self.snapcast_connector.close()
        self.handlers.discard(self)
        self._logger.info("Client disconnected")


    def on_socket_broadcast(self, events, message):

        try:
            self.write_message(message)
        except (RuntimeError, TypeError, NameError):
            traceback.print_exc(file=sys.stdout)
            self._logger.error("Runtime error in Websocket message handler")


    def on_socket_send(self, events, message):
        client = message['data']['client']
        if client and (client == self.request):
            del message['data']['client']
            self.write_message(message)


    def check_for_telnet_input(self):
        response = self.snapcast_connector.listen()
        if response:
            self._logger.debug('Websocket Broadcast: ' + str(response.strip().decode('utf8')))
            self.write_message(response)
