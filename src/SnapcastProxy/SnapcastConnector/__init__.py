import threading
import logging

class SnapTelnet(threading.Thread):
    def __init__(self, eventmanager):
        threading.Thread.__init__(self)
        self._logger = logging.getLogger(__name__)
