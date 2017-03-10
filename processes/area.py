
import json
import os
import subprocess
from pywps import Process, ComplexInput, LiteralOutput, Format
from pywps.wpsserver import temp_dir

__author__ = 'matteo'


class Area(Process):
    """Process calculating area of given polygon
    """
    def __init__(self):
        inputs = [ComplexInput('layer', 'Layer',
                               [Format('application/gml+xml')])]
        outputs = [LiteralOutput('area', 'Area', data_type='string')]

        super(Area, self).__init__(
            self._handler,
            identifier='area',
            title='Process Area',
            abstract="""Process returns the area of each
             feature from a submitted GML file""",
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        # ogr2ogr requires gdal-bin
        from shapely.geometry import shape
        with temp_dir() as tmp:
            input_gml = request.inputs['layer'][0].file
            input_geojson = os.path.join(tmp, 'input.geojson')
            subprocess.check_call(['ogr2ogr', '-f', 'geojson',
                                   str(input_geojson), input_gml])
            with open(input_geojson, 'rb') as f:
                data = json.loads(f.read())
            for feature in data['features']:
                geom = shape(feature['geometry'])
                feature['area'] = geom.area
            response.outputs['area'].data = [feature['area']
                                             for feature in data['features']]
            return response
