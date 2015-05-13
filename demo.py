#!/usr/bin/env python
import os, sys

sys.path.append(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    os.path.pardir))

from server import Server
from processes.sleep import Sleep
from processes.ultimate_question import UltimateQuestion
from processes.centroids import Centroids
from processes.sayhello import SayHello
from pywps import Process, ComplexInput, ComplexOutput, Format


def feature_count(request, response):
    import lxml.etree
    from pywps.app import xpath_ns

    doc = lxml.etree.parse(request.inputs['layer'])
    feature_elements = xpath_ns(doc, '//gml:featureMember')
    response.outputs['count'] = str(len(feature_elements))
    return response


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('listen', nargs='?', default='localhost:5000')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-w', '--waitress', action='store_true')
    args = parser.parse_args()

    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pywps.cfg")
    debug = args.debug
    host, port = args.listen.split(':')
    port = int(port)

    processes = [
        Process(feature_count,
                inputs=[ComplexInput('layer', 'Layer', [Format('SHP')])],
                outputs=[ComplexOutput('layer', 'Layer', [Format('GML')])]),
        SayHello(),
        Centroids(),
        UltimateQuestion(),
        Sleep()
    ]

    s = Server(host=host, port=port, debug=debug, processes=processes, config_file=config_file)

    # TODO: need to spawn a different process for different server
    if args.waitress:
        import waitress

        waitress.serve(s.app, host=host, port=port)
    else:
        s.run()


if __name__ == '__main__':
    main()
