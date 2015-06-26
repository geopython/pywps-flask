#!/usr/bin/env python
import flask
import multiprocessing
import os
import sys
from flask import request

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


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--waitress', action='store_true')
    args = parser.parse_args()

    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pywps.cfg")

    processes = [
        FeatureCount(),
        SayHello(),
        Centroids(),
        UltimateQuestion(),
        Sleep(),
        Buffer(),
        Area()
    ]

    # List of servers to start up
    server_list = [
        Server(processes=processes, host='0.0.0.0', port=5001, config_file=config_file),
        Server(processes=processes, host='0.0.0.0', port=5002)
    ]

    # List of server instances running
    server_instances = {}
    counter = 0
    for s in server_list:
        p = multiprocessing.Process(target=s.run)
        p.start()
        server_instances[counter] = {'Process': p, 'ServerObject': s}
        counter += 1

    if args.waitress:
        # TODO: make waitress use multiprocessing
        pass
        import waitress
        from pywps import configuration

        configuration.load_configuration(config_file)
        host = configuration.get_config_value('wps', 'serveraddress').split('://')[1]
        port = int(configuration.get_config_value('wps', 'serverport'))

        #waitress.serve(s.app, host=host, port=port)
    else:
        rest_app = flask.Flask(__name__)

        @rest_app.route('/rest/server', methods=['GET', 'PUT', 'DELETE'])
        def rest_servers():
            js = {}
            for s in server_instances:
                process = server_instances[s]['Process']
                server = server_instances[s]['ServerObject']
                json_server = {}
                json_server['pid'] = process.pid
                json_server['host'] = server.host
                json_server['port'] = server.port
                json_server['alive'] = process.is_alive()
                js[s] = json_server
            return flask.jsonify(js)

        @rest_app.route('/rest/server/<int:serverid>', methods=['GET', 'PUT', 'DELETE'])
        def rest_server(serverid):
            if request.method == 'GET':
                try:
                    process = server_instances[serverid]['Process']
                    server = server_instances[serverid]['ServerObject']
                    json_server = {}
                    json_server['pid'] = process.pid
                    json_server['host'] = server.host
                    json_server['port'] = server.port
                    json_server['alive'] = process.is_alive()
                    return flask.jsonify(json_server)
                except:
                    return 'GET ERROR'

            if request.method == 'PUT':
                try:
                    server_put = Server(processes=processes, host='0.0.0.0', port=5007)
                    server_list.append(server_put)

                    process_put = multiprocessing.Process(target=server_put.run)
                    process_put.start()
                    server_instances[serverid] = {'Process': process_put, 'ServerObject': server_put}
                    return 'Added new server with pid: %s' % (process_put.pid)
                except:
                    return 'PUT ERROR'

            if request.method == 'DELETE':
                try:
                    if serverid not in server_instances:
                        return 'Error... The specified server id doesn\'t exist'

                    process_delete = server_instances[serverid]['Process']
                    process_delete.terminate()
                    process_delete.join()
                    if process_delete.is_alive():
                        return 'Error terminating process: %s with pid: %s' % (serverid, process_delete.pid)
                    del server_instances[serverid]
                    return 'Deleted server with pid: %s' % (process_delete.pid)
                except Exception as e:
                    return 'DELETE ERROR: %s' % e

            return 'Unsupported Method'

        rest_app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
