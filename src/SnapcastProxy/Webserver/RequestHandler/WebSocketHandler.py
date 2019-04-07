import tornado.websocket
from tornado import gen, websocket, ioloop
import json
import sys
import logging
import traceback
from SnapcastProxy.SnapcastConnector.Telnet import SnapTelnet

class WebSocketHandler(websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):

        self.eventManager = kwargs.pop('eventmanager')
        self.handlers = kwargs.pop('wshandlers')
        self.socket_open = False
        self._logger = logging.getLogger(__name__)
        self.snapcast_connector = None
        self.finish_listener = False
        super(WebSocketHandler, self).__init__(*args, **kwargs)


    def check_origin(self, origin):
        return True


    def telnet_listen(self):
        response = self.snapcast_connector.listen()
        if response:
            self.write_message(response)

    def open(self):
        """
        initilized a new connection. here all config values etc. should be send to client
        """
        message = dict()
        message['client'] = self.request
        self.socket_open = True
        self.handlers.add(self)
        self._logger.info("New client connected")
        self.snapcast_connector = SnapTelnet(self.eventManager)
        self.pCallback = tornado.ioloop.PeriodicCallback(self.telnet_listen, callback_time=10)
        self.pCallback.start()

    def close_callback(self):
        pass

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
        self.finish_listener = True
        self.socket_open = False
        self.pCallback.stop()
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

