from tornado.concurrent import return_future
from tornado.httpclient import HTTPRequest, HTTPResponse

from .collection import RequestCollection

class AsyncHTTPStubClient(object):

    @return_future
    def fetch(self, request, callback=None, **kwargs):
        if not isinstance(request, HTTPRequest):
            request = HTTPRequest(url=request, **kwargs)
        response_partial = RequestCollection.find(request)
        if response_partial:
            resp = response_partial(request)
        else:
            resp = HTTPResponse(request, 404)
        callback(resp)
