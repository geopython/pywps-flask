
from pywps import Process, LiteralInput, \
        ComplexInput, ComplexOutput, Format, FORMATS


from pywps.validator.mode import MODE

__author__ = 'Brauni'


class Buffer(Process):
    def __init__(self):
        inputs = [ComplexInput('poly_in', 'Input vector file',
                  supported_formats=[Format('application/gml+xml')],
                  mode=MODE.STRICT),
                  LiteralInput('buffer', 'Buffer size', data_type='float',
                  allowed_values=(0, 1, 10, (10, 10, 100), (100, 100, 1000)))]
        outputs = [ComplexOutput('buff_out', 'Buffered file',
                                 supported_formats=[
                                            Format('application/gml+xml')
                                            ]
                                 )]

        super(Buffer, self).__init__(
            self._handler,
            identifier='buffer',
            version='0.1',
            title="GDAL Buffer process",
            abstract="""The process returns buffers around the input features,
             using the GDAL library""",
            profile='',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        from osgeo import ogr

        inSource = ogr.Open(request.inputs['poly_in'][0].file)

        inLayer = inSource.GetLayer()
        out = inLayer.GetName() + '_buffer'

        # create output file
        driver = ogr.GetDriverByName('GML')
        outSource = driver.CreateDataSource(
                                out,
                                ["XSISCHEMAURI=\
                            http://schemas.opengis.net/gml/2.1.2/feature.xsd"])
        outLayer = outSource.CreateLayer(out, None, ogr.wkbUnknown)

        # for each feature
        featureCount = inLayer.GetFeatureCount()
        index = 0

        while index < featureCount:
            # get the geometry
            inFeature = inLayer.GetNextFeature()
            inGeometry = inFeature.GetGeometryRef()

            # make the buffer
            buff = inGeometry.Buffer(float(request.inputs['buffer'][0].data))

            # create output feature to the file
            outFeature = ogr.Feature(feature_def=outLayer.GetLayerDefn())
            outFeature.SetGeometryDirectly(buff)
            outLayer.CreateFeature(outFeature)
            outFeature.Destroy()  # makes it crash when using debug
            index += 1

            response.update_status('Buffering', 100*(index/featureCount))

        outSource.Destroy()

        response.outputs['buff_out'].output_format = FORMATS.GML
        response.outputs['buff_out'].file = out

        return response
