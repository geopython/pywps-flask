from pywps import Process, LiteralInput, LiteralOutput


class SayHello(Process):
    def __init__(self):
        inputs = [LiteralInput('name', 'Input name', data_type='string')]
        outputs = [LiteralOutput('response', 'Output response', data_type='string')]

        super(SayHello, self).__init__(
            self._handler,
            identifier='say_hello',
            title='Process Say Hello',
            version='1.3.3.7',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    @staticmethod
    def _handler(request, response):
        response.outputs['response'].data = 'Hello ' + request.inputs['name'].data
        return response