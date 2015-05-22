import json
import os
import subprocess
from pywps import Process, ComplexInput, ComplexOutput, Format, FORMATS
from pywps.wpsserver import temp_dir


class Centroids(Process):
    def __init__(self):
        inputs = [ComplexInput('layer', 'Layer', [Format('GML')])]
        outputs = [ComplexOutput('out', 'Referenced Output', [Format('JSON')])]

        super(Centroids, self).__init__(
            self._handler,
            identifier='centroids',
            title='Process Centroids',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    @staticmethod
    def _handler(request, response):
         # ogr2ogr requires gdal-bin
        from shapely.geometry import shape, mapping

        with temp_dir() as tmp:
            input_gml = request.inputs['layer'].file
            input_geojson = os.path.join(tmp, 'input.geojson')
            subprocess.check_call(['ogr2ogr', '-f', 'geojson',
                                   input_geojson, input_gml])
            data = json.loads(input_geojson.read_file('r'))
            for feature in data['features']:
                geom = shape(feature['geometry'])
                feature['geometry'] = mapping(geom.centroid)
            out_bytes = json.dumps(data, indent=2)
            response.outputs['out'].output_format = Format(FORMATS['JSON'])
            response.outputs['out'].data = out_bytes
            return response