__author__ = 'matteo'

import json
import os
import subprocess
from pywps import Process, ComplexInput, LiteralOutput, Format
from pywps.wpsserver import temp_dir


class Area(Process):
    def __init__(self):
        inputs = [ComplexInput('layer', 'Layer', [Format('GML')])]
        outputs = [LiteralOutput('area', data_type='string')]

        super(Area, self).__init__(
            self._handler,
            identifier='area',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    @staticmethod
    def _handler(request, response):
         # ogr2ogr requires gdal-bin
        from shapely.geometry import shape
        with temp_dir() as tmp:
            input_gml = request.inputs['layer'].file
            input_geojson = os.path.join(tmp, 'input.geojson')
            subprocess.check_call(['ogr2ogr', '-f', 'geojson',
                                   str(input_geojson), input_gml])
            data = json.loads(input_geojson.read_file('r'))
            features = []
            for feature in data['features']:
                geom = shape(feature['geometry'])
                feature['area'] = geom.area
            response.outputs['area'].data = [ feature['area'] for feature in data['features']]
            return response