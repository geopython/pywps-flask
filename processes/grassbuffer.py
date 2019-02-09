
from pywps import Process, LiteralInput, ComplexInput, ComplexOutput, Format


from pywps.validator.mode import MODE

__author__ = 'Jachym'


class GrassBuffer(Process):
    
    def __init__(self):
        inputs = [ComplexInput('poly_in', 'Input1',
                  supported_formats=[Format('application/gml+xml')],
                  mode=MODE.SIMPLE),
                  LiteralInput('buffer', 'Buffer', data_type='float',
                  allowed_values=(0, 1, 10, (10, 10, 100), (100, 100, 1000)))]
        outputs = [ComplexOutput('buff_out', 'Buffered',
                                 supported_formats=[
                                                Format('application/gml+xml')
                                                    ])]

        super(GrassBuffer, self).__init__(
            self._handler,
            identifier='grassbuffer',
            version='0.1',
            title="GRASS v.buffer",
            abstract='The process uses the  GRASS GIS \
             v.buffer module to generate buffers around inputs ',
            profile='',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True,
            # grass_location="/tmp/outputs/pyws_process_GMkyxP/pywps_location"
            grass_location="epsg:3857"
        )

    def _handler(self, request, response):

        from grass.pygrass.modules import Module
        Module('v.import',
               input=request.inputs['poly_in'][0].file,
               epsg=3857, output='poly', extent='input')
        Module('v.buffer',
               input='poly',
               distance=request.inputs['buffer'][0].data,
               output='buffer')
        Module('v.out.ogr', input='buffer', output='buffer.gml', format='GML')

        response.outputs['buff_out'].file = 'buffer.gml'

        return response
