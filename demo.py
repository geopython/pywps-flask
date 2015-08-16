#!/usr/bin/env python
import flask
import multiprocessing
import os
import psutil
import sys
from flask import request
from werkzeug.wrappers import Response

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

    from pywps import configuration
    # TODO: the config file should be "global" to a single server instance and not across all
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pywps.cfg")
    configuration.load_configuration(config_file)
    rest_url = '/wpsadmin'

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
    for s in server_list:
        p = multiprocessing.Process(target=s.run)
        p.start()
        server_instances[p.pid] = {'Process': p, 'ServerObject': s}

    if args.waitress:
        # TODO: make waitress use multiprocessing
        pass
        import waitress

        host = configuration.get_config_value('wps', 'serveraddress').split('://')[1]
        port = int(configuration.get_config_value('wps', 'serverport'))

        #waitress.serve(s.app, host=host, port=port)
    else:
        rest_app = flask.Flask(__name__)

        @rest_app.route(rest_url)
        def rest_index():
            return flask.Response('REST Interface<br/>'
                                  'List of REST url:<br/>'
                                  '<p>...'+rest_url+'/configuration<br/>'
                                  '<p>&emsp;[GET]<br/>&emsp;Returns a list of all server instance configuration'
                                  '</p>'

                                  '<p>...'+rest_url+'/configuration/&#60int:serverid&#62<br/>'
                                  '<p>&emsp;[GET]<br/>&emsp; Returns the configuration of serverid server instance</p>'
                                  '<p>&emsp;[PUT]<br/>&emsp; Changes specific configuration of serverid server instance.'
                                  ' (Passed data must be JSON formatted and submitted with Header Content-Type application/json)</p>'
                                  '</p>'
                                  '<p>...'+rest_url+'/server<br/>'
                                  '<p>&emsp;[GET]<br/>&emsp; Returns a list of server instances containing information about the host, port, pid and process status</p>'
                                  '</p>'

                                  '<p>...'+rest_url+'/server/&#60int:serverid&#62<br/>'
                                  '<p>&emsp;[GET]<br/>&emsp; Returns the host, port, pid and process status of serverid server instance.</p>'
                                  '<p>&emsp;[PUT]<br/>&emsp; Creates and starts a new serverid server instances specified by the passed data.'
                                  ' (Passed data must be JSON formatted and submitted with Header Content-Type application/json)</p>'
                                  '<p>&emsp;[DELETE]<br/>&emsp; Stops and removes serverid server instances from currently available server instances.</p>'
                                  '</p>'

                                  '<p>...'+rest_url+'/server/&#60int:serverid&#62/pause<br/>'
                                  '<p>&emsp;[GET]<br/>&emsp; Pauses the server instance specified by serverid.</p>'
                                  '</p>'

                                  '<p>...'+rest_url+'/server/&#60int:serverid&#62/resume<br/>'
                                  '<p>&emsp;[GET]<br/>&emsp; Resumes the server instance specified by serverid.</p>'
                                  '</p>'
                                  )

        @rest_app.route(rest_url+'/configuration', methods=['GET'])
        def rest_configuration():
            js = {}
            for s in server_instances:
                process = server_instances[s]['Process']
                server = server_instances[s]['ServerObject']
                json_server = {}
                config = server.get_configuration()
                for section in config.sections():
                    for (key, val) in config.items(section):
                        json_server[key] = val
                js[process.pid] = json_server
            response = flask.jsonify(js)
            response.status_code = 200
            return response

        @rest_app.route(rest_url+'/configuration/<int:serverid>', methods=['GET', 'PUT'])
        def rest_config(serverid):
            if request.method == 'GET':
                try:
                    process = server_instances[serverid]['Process']
                    server = server_instances[serverid]['ServerObject']
                    json_server = {}
                    config = server.get_configuration()
                    for section in config.sections():
                        for (key, val) in config.items(section):
                            json_server[key] = val
                    response = flask.jsonify(json_server)
                    response.status_code = 200
                    return response
                except:
                    return Response(status=500)
            elif request.method == 'PUT':
                try:
                    # only parse json and if Header Content-Type is application/json
                    data = request.get_json()

                    #  TODO: check if configuration key is valid

                    server = server_instances[serverid]['ServerObject']
                    config = server.get_configuration()

                    for section in config.sections():
                        for (key, val) in config.items(section):
                            if key in data:
                                config.set(section, key, data[key])

                    # remove running instance so we can create an updated version
                    if serverid in server_instances:
                        _terminate_process(serverid)

                    # create and add process
                    server_put = Server(processes=processes)
                    server_put.set_configuration(config)
                    process_put = multiprocessing.Process(target=server_put.run)
                    process_put.start()
                    server_instances[serverid] = {'Process': process_put, 'ServerObject': server_put}
                    return Response(status=201)
                except:
                    return Response(status=500)

        @rest_app.route(rest_url+'/server/<int:serverid>/pause', methods=['GET'])
        def rest_stop_server(serverid):
            if request.method == 'GET':
                try:
                    p = psutil.Process(serverid)

                    if p.status == psutil.STATUS_RUNNING or p.status == psutil.STATUS_SLEEPING:
                        p.suspend()
                        return Response('Suspended running Server with PID %s' % serverid, status=200)
                    else:
                        return Response('Server with PID %s already suspended' % serverid, status=200)
                except:
                    return Response(status=500)

        @rest_app.route(rest_url+'/server/<int:serverid>/resume', methods=['GET'])
        def rest_resume_server(serverid):
            if request.method == 'GET':
                try:
                    p = psutil.Process(serverid)

                    if p.status == psutil.STATUS_STOPPED:
                        p.resume()
                        return Response('Resumed suspended Server with PID %s' % serverid, status=200)
                    else:
                        return Response('Server with PID %s already resumed' % serverid, status=200)
                except:
                    return Response(status=500)

        @rest_app.route(rest_url+'/server', methods=['GET'])
        def rest_servers():
            js = {}
            for s in server_instances:
                process = server_instances[s]['Process']
                server = server_instances[s]['ServerObject']

                p = psutil.Process(process.pid)

                json_server = {}
                json_server['pid'] = process.pid
                json_server['host'] = server.host
                json_server['port'] = server.port
                json_server['status'] = p.status
                js[s] = json_server
            response = flask.jsonify(js)
            response.status_code = 200
            return response

        @rest_app.route(rest_url+'/server/<int:serverid>', methods=['GET', 'PUT', 'DELETE'])
        def rest_server(serverid):
            if request.method == 'GET':
                try:
                    process = server_instances[serverid]['Process']
                    server = server_instances[serverid]['ServerObject']

                    p = psutil.Process(serverid)

                    json_server = {}
                    json_server['pid'] = process.pid
                    json_server['host'] = server.host
                    json_server['port'] = server.port
                    json_server['status'] = p.status
                    response = flask.jsonify(json_server)
                    response.status_code = 200
                    return response
                except:
                    return Response(status=500)

            if request.method == 'PUT':
                try:
                    # only parse json and if Header Content-Type is application/json
                    data = request.get_json()

                    if 'host' not in data:
                        return Response(response='No host specified!', status=400)

                    if 'port' not in data:
                        return Response(response='No port specified!', status=400)

                    # remove running instance so we can create an updated version
                    if serverid in server_instances:
                        _terminate_process(serverid)

                    # create and add process
                    server_put = Server(processes=processes, host=data['host'], port=data['port'])
                    process_put = multiprocessing.Process(target=server_put.run)
                    process_put.start()
                    server_instances[serverid] = {'Process': process_put, 'ServerObject': server_put}
                    return Response(status=201)
                except:
                    return Response(status=500)

            if request.method == 'DELETE':
                try:
                    if serverid in server_instances:
                        _terminate_process()
                    return Response(status=200)
                except Exception as e:
                    return Response(status=500)

            return Response(status=405)

        # Terminates a process and removes it from the list
        def _terminate_process(serverid):
            process_delete = server_instances[serverid]['Process']
            process_delete.terminate()
            process_delete.join()
            if process_delete.is_alive():
                return Response(response='Error terminating process: %s with pid: %s' % (serverid, process_delete.pid), status=500)
            del server_instances[serverid]

        rest_app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
