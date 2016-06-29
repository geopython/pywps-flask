from pywps import Process, ComplexInput, Format, LiteralOutput


class FeatureCount(Process):
    def __init__(self):
        inputs = [ComplexInput('layer', 'Layer', [Format('application/gml+xml')])]
        outputs = [LiteralOutput('count', 'Count', data_type='integer')]

        super(FeatureCount, self).__init__(
            self._handler,
            identifier='feature_count',
            version='None',
            title='Feature count',
            abstract='This process counts the number of features in a vector',
            profile='',
            metadata=['Feature', 'Count'],
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        import lxml.etree
        from pywps.app.basic import xpath_ns
        doc = lxml.etree.parse(request.inputs['layer'][0].file)
        feature_elements = xpath_ns(doc, '//gml:featureMember')
        response.outputs['count'].data = len(feature_elements)
        return response
