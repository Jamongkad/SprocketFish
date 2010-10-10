import web
from webob import Request as WebRequest

class Request(object):
    def __init__(self):
        self.input_data = web.data()
        self.env        = web.ctx.env
        self.POST       = self.POST()

    def POST(self):
        req        = WebRequest(self.env)
        req.method = 'POST'
        req.body   = self.input_data
        return req.POST

