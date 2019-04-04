__author__ = "Mario Lukas"
__copyright__ = "Copyright 2017"
__license__ = "GPL v2"
__maintainer__ = "Mario Lukas"
__email__ = "info@mariolukas.de"

import threading
import tornado
import tornado.ioloop
import tornado.web
import logging
import time
import os
import datetime
import asyncio
from tornado import gen

from SnapcastProxy.Webserver.RequestHandler.StaticFileHandler import StaticFileHandler
from SnapcastProxy.Webserver.RequestHandler.WebSocketHandler import WebSocketHandler
from SnapcastProxy.Webserver.RequestHandler.JSONrpcHandler import JSONrpcHandler

class WebServer(threading.Thread):

    def __init__(self, eventmanager):
        threading.Thread.__init__(self)
        self.exit = False
        self.eventmanager = eventmanager
        #self.snapcast_connector = snapcast_connector
        self.www_folder = '/var/www'
        self._logger = logging.getLogger(__name__)
        self.websocket_handlers = set()

    def routes(self):
        return tornado.web.Application([
            (r'/jsonrpc', JSONrpcHandler, dict(eventmanager=self.eventmanager)),
            (r'/websocket', WebSocketHandler, dict(eventmanager=self.eventmanager, wshandlers=self.websocket_handlers)),
            (r"/(.*)", StaticFileHandler, {"path": self.www_folder, "default_filename": "index.html"})
        ])

    #@tornado.gen.coroutine
    async def auto_loop(self):
        while True:
           if len(self.websocket_handlers) > 0:
                for handler in self.websocket_handlers:
                    handler.check_for_telnet_input()
           await gen.sleep(0.05)

    def run(self):
        self._logger.info("Starting Webserver")
        asyncio.set_event_loop(asyncio.new_event_loop())

        tornado.ioloop.IOLoop.current().spawn_callback(self.auto_loop)
        webserver = self.routes()
        webserver.listen(8080)
        tornado.ioloop.IOLoop.current().start()



    def kill(self):
        tornado.ioloop.IOLoop.instance().stop()