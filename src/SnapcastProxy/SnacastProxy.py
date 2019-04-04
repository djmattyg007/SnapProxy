import argparse
import os
import signal
import logging
import time
from SnapcastProxy.EventManager.Events import EventManager
from SnapcastProxy.Webserver.WebServer import WebServer
from SnapcastProxy.SnapcastConnector.Telnet import SnapTelnet

DEFAULT_LISTENPORT  =  7777
DEFAULT_PORT_SNAPCAST = 1705
VERSION = "0.0.1"
AUTHOR="Mario Lukas"

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", action="store_true", dest="debug", default=False, help="add verbosity")
parser.add_argument("-p", "--port", nargs=1, dest="port", help="default is " + str(DEFAULT_LISTENPORT))
parser.add_argument("-s", "--snapcastPort", nargs=1, dest="snapcast_port", help="snapcast port")
parser.add_argument("-l", "--log", nargs=1, dest="log", default=False, help=" path file to save log")
parser.add_argument('-v', '--version', action='version', version=VERSION + "\n" + AUTHOR)

def handler(signum, frame):
    print('\r\nLeaving Snapcast Proxy. Bye.')
    os._exit(0)


if __name__ == '__main__':


    signal.signal(signal.SIGINT, handler)
    args = parser.parse_args()

    portHttp = DEFAULT_LISTENPORT
    snapPort = DEFAULT_PORT_SNAPCAST

    log = logging.getLogger()

    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    log_level = logging.DEBUG

    if args.log:
        logging.basicConfig(filename=args.log[0],
                            filemode='w',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%H:%M:%S',
                            level=log_level)
    else:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%H:%M:%S',
                            level=log_level)
    if args.port:
        log.info("Listenning on port:" + str(args.port[0]))
        portHttp = int(args.port[0])

    if args.snapcast_port:
        log.info("setting Snapcast port to: " + str(args.httsport[0]))
        snapPort = int(args.httsport[0])

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger=logging.getLogger("SnapCastProxy")

    log_level= {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING
    }


    logging.info("Starting Snapcast Proxy")
    eventmanager = EventManager()

    #snapcast_connector = SnapTelnet(eventmanager)
    #snapcast_connector.start()

    webserver = WebServer(eventmanager)
    webserver.start()

    # server forever
    while(1):
        time.sleep(0.5)

    os._exit(0)