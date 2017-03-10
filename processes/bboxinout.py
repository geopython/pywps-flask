
from pywps import Process, BoundingBoxInput, BoundingBoxOutput

__author__ = 'Jachym'


class Box(Process):
    def __init__(self):
        inputs = [BoundingBoxInput('bboxin',
                                   'box in', ['epsg:4326', 'epsg:3035'])]
        outputs = [BoundingBoxOutput('bboxout',
                                     'box out', ['epsg:4326'])]

        super(Box, self).__init__(
            self._handler,
            identifier='boundingbox',
            version='0.1',
            title="Bounding box in- and out",
            abstract="""Given a  bounding box, it
             returns the same bounding box""",
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        response.outputs['bboxout'].data = request.inputs['bboxin'][0].data

        return response
