import os
import flask
from pywps import Service, Process, ComplexInput, Format, ComplexOutput, FORMATS, LiteralOutput, LiteralInput
from pywps.wpsserver import PyWPSServerAbstract, temp_dir
from pywps import config


class Server(PyWPSServerAbstract):
    def __init__(self, host='localhost', port='5000', debug=False, processes=[], config_file=None):
        self.app = flask.Flask(__name__)
        self.host = host
        self.port = port
        self.debug = debug

        # Load config files and override settings if any file specified
        if config_file:
            config.load_configuration(config_file)

        self.output_url = config.get_config_value('server', 'outputUrl')
        self.output_path = config.get_config_value('server', 'outputPath')
        self.temp_path = config.get_config_value('server', 'tempPath')
        self.host = config.get_config_value('wps', 'serveraddress').split('://')[1]
        self.port = int(config.get_config_value('wps', 'serverport'))

        self.processes = processes

        self.service = Service(processes=self.processes)

    def run(self):
        @self.app.route('/')
        def index():
            url = flask.url_for('wps', _external=True)
            return flask.render_template('home.html', url=url)

        @self.app.route('/wps', methods=['GET', 'POST'])
        def wps():
            return self.service

        @self.app.route(self.output_url+'<uuid>')
        def datafile(uuid):
            for data_file in os.listdir(self.output_path):
                if data_file == uuid:
                    file_ext = os.path.splitext(data_file)[1]
                    file_obj = open(os.path.join(self.output_path, data_file))
                    file_bytes = file_obj.read()
                    file_obj.close()
                    mime_type = None
                    if 'xml' in file_ext:
                        mime_type = 'text/xml'
                    return flask.Response(file_bytes, content_type=mime_type)
            else:
                flask.abort(404)

        self.app.run(host=self.host, port=self.port, debug=self.debug)
