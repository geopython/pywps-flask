#!/usr/bin/env python
import os
import sys

# CAUTION! This line is only used for a development environment, when pywps is not installed
sys.path.append(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    os.path.pardir))

from server import Server
from processes.sleep import Sleep
from processes.ultimate_question import UltimateQuestion
from processes.centroids import Centroids
from processes.sayhello import SayHello
from processes.feature_count import FeatureCount
from processes.buffer import Buffer
from processes.area import Area
from processes.bboxinout import Box


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--waitress', action='store_true')
    parser.add_argument('-d', '--daemon', action='store_true')
    args = parser.parse_args()

    if args.daemon:
        pid = None
        try:
            pid = os.fork()
        except OSError as e:
             raise Exception, "%s [%d]" % (e.strerror, e.errno)

        if (pid == 0):
            os.setsid()
            start(args)
        else:
            os._exit(0)

    else:
        start(args)

def start(args, kill = None):
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pywps.cfg")

    processes = [
        FeatureCount(),
        SayHello(),
        Centroids(),
        UltimateQuestion(),
        Sleep(),
        Buffer(),
        Area(),
        Box()
    ]

    s = Server(processes=processes, config_file=config_file)

    # TODO: need to spawn a different process for different server
    if args.waitress:
        import waitress
        from pywps import configuration

        configuration.load_configuration(config_file)
        host = configuration.get_config_value('wps', 'serveraddress').split('://')[1]
        port = int(configuration.get_config_value('wps', 'serverport'))

        waitress.serve(s.app, host=host, port=port)
    else:
        s.run()


if __name__ == '__main__':
    main()
