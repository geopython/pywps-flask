import os
import tempfile

__author__ = 'Jachym'

from pywps import Process, BoundingBoxInput, BoundingBoxOutput


class Box(Process):
    def __init__(self):
        inputs = [BoundingBoxInput('bboxin', 'box in', ['epsg:4326', 'epsg:3035'])]
        outputs = [BoundingBoxOutput('bboxout', 'box out', ['epsg:4326'])]

        super(Box, self).__init__(
            self._handler,
            identifier='boundingbox',
            version='0.1',
            title="Bounding box in- and out",
            abstract='Give bounding box, return the same',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        response.outputs['bboxout'].data = request.inputs['bboxin'].data

        return response

