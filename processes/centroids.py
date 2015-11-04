import json
import os
import subprocess
from pywps import Process, ComplexInput, ComplexOutput, Format, FORMATS
from pywps.wpsserver import temp_dir


class Centroids(Process):
    def __init__(self):
        inputs = [ComplexInput('layer', 'Layer',
            supported_formats=[Format('application/gml+xml')])]
        outputs = [ComplexOutput('out', 'Referenced Output',
            supported_formats=[Format('application/json')])]

        super(Centroids, self).__init__(
            self._handler,
            identifier='centroids',
            title='Process Centroids',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
         # ogr2ogr requires gdal-bin
        from shapely.geometry import shape, mapping

        with temp_dir() as tmp:
            input_gml = request.inputs['layer'].file
            input_geojson = os.path.join(tmp, 'input.geojson')
            subprocess.check_call(['ogr2ogr', '-f', 'geojson',
                                   input_geojson, input_gml])
            with open(input_geojson, 'rb') as f:
                data = json.loads(f.read())
            for feature in data['features']:
                geom = shape(feature['geometry'])
                feature['geometry'] = mapping(geom.centroid)
            out_bytes = json.dumps(data, indent=2)
            response.outputs['out'].output_format = Format(FORMATS['JSON'])
            response.outputs['out'].data = out_bytes
            return response
