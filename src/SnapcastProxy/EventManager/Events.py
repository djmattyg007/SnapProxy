__author__ = "Mario Lukas"
__copyright__ = "Copyright 2017"
__license__ = "GPL v2"
__maintainer__ = "Mario Lukas"
__email__ = "info@mariolukas.de"

from queue import Queue
from queue import Empty
import logging



class Events(object):
    ON_BROADCAST = "ON_BROADCAST"
    ON_SOCKET_SEND = "ON_WEBSOCKET_SEND"
    ON_TELNET_SEND = "ON_TELNET_SEND"
    ON_TELNET_RECEIVE = "ON_TELNET_RECIVE"
    ON_CLIENT_CONNECTED = "ON_CLIENT_CONNECTED"

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class EventManager(metaclass=Singleton):

    # # make it sinleton
    # _instance = None
    # def __new__(cls, *args, **kwargs):
    #     if not cls._instance:
    #         cls._instance = super(Singleton, cls).__new__(
    #                             cls, *args, **kwargs)
    #     return cls._instance

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.reset()
        self.event_q = Queue()
        self._logger.info('Event Manager initialized')

    def subscribe(self, key, callback, force=False):

        if key not in self.subscriptions:
            self.subscriptions[key] = []

        subscription = {
            'key': key,
            'callback': callback
        }

        if force or not self.has_subscription(key, callback):
            self.subscriptions[key].append(subscription)

        return self

    def unsubscribe(self, key, callback):
        if not self.has_subscription(key, callback):
            return self

        self.subscriptions[key].remove({
            'key': key,
            'callback': callback
        })

    def unsubscribe_all(self, key):
        if key not in self.subscriptions:
            return self

        self.subscriptions[key] = []

    def has_subscription(self, key, callback):
        if key not in self.subscriptions:
            return False

        subscription = {
            'key': key,
            'callback': callback
        }

        return subscription in self.subscriptions[key]

    def has_any_subscriptions(self, key):
        return key in self.subscriptions and len(self.subscriptions[key]) > 0

    def publish(self, key, *args, **kwargs):
        if not self.has_any_subscriptions(key):
            return self

        for subscriber in self.subscriptions[key]:
            subscriber['callback'](self, *args, **kwargs)

    def reset(self):
        self.subscriptions = {}

    def handle_event_q(self):
        if not self.event_q.empty():
            try:
                event = self.event_q.get_nowait()
                self.publish(event['event'], event['data'])

            except Empty:
                    pass
        pass

    def get_event_q(self):
        return self.event_q
